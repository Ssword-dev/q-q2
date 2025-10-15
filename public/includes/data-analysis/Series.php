<?php

namespace Ssword\DataAnalysis;

use InvalidArgumentException;
use Iterator;
use ArrayAccess;
use Countable;

/**
 * A series for data analysis.
 */
class Series implements ArrayAccess, Iterator, Countable
{
    /** @var array */
    private array $data;

    /** @var array|null */
    private ?array $index;

    /** @var int */
    private int $position = 0;

    public function __construct(array $data = [], ?array $index = null)
    {
        $this->data = array_values($data); // get only the values.

        if ($index !== null) {
            if (count($index) !== count($data)) {
                throw new InvalidArgumentException("Index length must match data length");
            }
            $this->index = $index;
        } else {
            $this->index = range(0, count($data) - 1);
        }
    }

    // statitics.

    /**
     * 
     * @return float
     */
    public function mean(): float
    {
        if (empty($this->data)) {
            return 0.0;
        }

        return (float) ($this->sum() / count($this->data));
    }

    /**
     * gets the median of the series.
     * this is the combination of the two middle values
     * if even, then the middle value if odd.
     * @return float
     */
    public function median(): float
    {
        if (empty($this->data)) {
            return 0.0;
        }

        $values = $this->data;
        sort($values);
        $count = count($values);

        if ($count % 2 === 0) {
            return ($values[$count / 2 - 1] + $values[$count / 2]) / 2;
        }

        return $values[floor($count / 2)];
    }

    /**
     * returns null for empty series.
     * returns the most frequently occuring item.
     * @return mixed|null
     */
    public function mode()
    {
        if (empty($this->data)) {
            return null;
        }

        // objects are not serializable in a fast way.
        // so imma use this keyToValue table.
        $keyToValue = [];
        $occurrence = [];

        foreach ($this->data as $item) {
            // serialize non primitive data.
            $key = is_object($item) ? ('o:' . spl_object_id($item)) : ('v:' . serialize($item));


            if (isset($occurrence[$key])) {
                $occurrence[$key]++;
            } else {
                $occurrence[$key] = 1;
                $keyToValue[$key] = $item;
            }
        }

        // determine the highest occurence.
        $modes = [];
        $highest = 0;

        foreach ($occurrence as $key => $count) {
            if ($count > $highest) {
                $highest = $count;
                $modes = [$keyToValue[$key]];
            } elseif ($count === $highest) {
                $modes[] = $keyToValue[$key];
            }
        }

        if (count($modes) === 0) {
            return null;
        }

        return count($modes) === 1 ? $modes[0] : $modes;
    }

    public function variance()
    {
        $mean = $this->mean();
        return array_reduce($this->data, function ($acc, $item) use ($mean) {
            return $acc + pow($item - $mean, 2);
        }, 0) / count($this->data);
    }

    /**
     * @return float total absolute deviation.
     */
    public function tad()
    {
        $mean = $this->mean();
        return (float) array_reduce($this->data, function ($acc, $item) use ($mean) {
            return $acc + abs($item - $mean);
        }, 0);
    }

    /**
     * gets the standard deviation.
     * @return float
     */
    public function std(): float
    {
        if (empty($this->data)) {
            return 0.0; // no variance.
        }

        return (float) sqrt($this->variance());
    }

    /**
     * @return float the mean of the total absolute deviation. or mean absolute deviation.
     */
    public function mad(): float
    {
        if (empty($this->data)) {
            return 0.0; // no variance.
        }

        return (float) $this->tad() / count($this->data);
    }


    /**
     * @return float the sum of all elements. is the sigma from i=0 to i=(|this|-1).
     */
    public function sum(): float
    {
        return (float) array_sum($this->data);
    }

    /**
     * @return float the minimum value.
     */
    public function min(): float
    {
        return (float) min($this->data);
    }

    /**
     * @return float the maximum value.
     */
    public function max(): float
    {
        return (float) max($this->data);
    }

    // array-like methods.
    // gives the convinience of array. but
    // with the extra convinience of being a series.
    // plus, this makes it javascript like (: big win.

    /**
     * like `Array.filter` in javascript.
     * @param callable $callback
     * @return Series
     */
    public function filter(callable $callback): Series
    {
        $filtered = array_filter($this->data, $callback);
        $filteredIndex = array_intersect_key($this->index, $filtered);
        return new Series(array_values($filtered), array_values($filteredIndex));
    }

    /**
     * like `Array.map` in javascript.
     * @param callable $callback
     * @return Series
     */
    public function map(callable $callback): Series
    {
        return new Series(array_map($callback, $this->data), $this->index);
    }

    /**
     * @param bool $ascending when true, lowest value first. else, highest value first.
     * @return Series a sorted series.
     */
    public function sort(bool $ascending = true): Series
    {
        $data = $this->data;
        $index = $this->index;
        array_multisort($data, $ascending ? SORT_ASC : SORT_DESC, $index);
        return new Series($data, $index);
    }

    // ArrayAccess
    // magical methods that php internally calls
    // when using array syntactic sugars. like indexing.
    public function offsetExists(mixed $offset): bool
    {
        return isset($this->data[$this->getDataIndex($offset)]);
    }

    public function offsetGet(mixed $offset): mixed
    {
        $idx = $this->getDataIndex($offset);
        if (!isset($this->data[$idx])) {
            throw new InvalidArgumentException("Invalid index: $offset");
        }
        return $this->data[$idx];
    }

    public function offsetSet(mixed $offset, mixed $value): void
    {
        if ($offset === null) {
            throw new InvalidArgumentException("Cannot append to Series - use reindex() to change size");
        }

        $idx = $this->getDataIndex($offset);
        if (!isset($this->data[$idx])) {
            throw new InvalidArgumentException("Invalid index: $offset");
        }
        $this->data[$idx] = $value;
    }

    public function offsetUnset(mixed $offset): void
    {
        throw new InvalidArgumentException("Cannot unset Series values - use filter() to remove elements");
    }

    // Iterator
    // enables iteration using loops like foreach.
    public function current(): mixed
    {
        return $this->data[$this->position];
    }

    public function key(): mixed
    {
        return $this->index[$this->position];
    }

    public function next(): void
    {
        $this->position++;
    }

    public function rewind(): void
    {
        $this->position = 0;
    }

    public function valid(): bool
    {
        return isset($this->data[$this->position]);
    }

    // Countable

    public function count(): int
    {
        return count($this->data);
    }

    // Helper Methods
    // used internally to not bloat the file.
    private function getDataIndex(mixed $offset): int
    {
        if (is_int($offset)) {
            if ($offset < 0 || $offset >= count($this->data)) {
                throw new InvalidArgumentException("Index out of bounds: $offset");
            }
            return $offset;
        }

        $idx = array_search($offset, $this->index, true);
        if ($idx === false) {
            throw new InvalidArgumentException("Index not found: $offset");
        }
        return $idx;
    }

    /**
     * first n items.
     * @param int $n is the number of items.
     * @return Series a series containing the first n items.
     */
    public function head(int $n): Series
    {
        return new Series(
            array_slice($this->data, 0, $n),
            array_slice($this->index, 0, $n)
        );
    }

    public function tail(int $n): Series
    {
        return new Series(
            array_slice($this->data, -$n),
            array_slice($this->index, -$n)
        );
    }

    /**
     * convert series to a normal array
     * @return array
     */
    public function toArray(): array
    {
        return $this->data;
    }

    /**
     * get the index array
     * @return array
     */
    public function getIndex(): array
    {
        return $this->index;
    }
}