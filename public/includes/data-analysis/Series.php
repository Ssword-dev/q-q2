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

    public function mean(): float
    {
        if (empty($this->data)) {
            return 0.0;
        }
        return array_sum($this->data) / count($this->data);
    }

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
     * Return the mode (most frequent value) of the series.
     * Supports scalar values, arrays and objects (objects are counted by identity).
     * Returns null for empty series, the single mode value if unique, or an array of modes when tied.
     *
     * @return mixed|null
     */
    public function mode()
    {
        if (empty($this->data)) {
            return null;
        }

        // the key to value array is because objects are not serializable.
        // in a fast way.
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

    public function sum(): float
    {
        return array_sum($this->data);
    }

    public function min(): float
    {
        return min($this->data);
    }

    public function max(): float
    {
        return max($this->data);
    }

    // Data Manipulation

    public function filter(callable $callback): Series
    {
        $filtered = array_filter($this->data, $callback);
        $filteredIndex = array_intersect_key($this->index, $filtered);
        return new Series(array_values($filtered), array_values($filteredIndex));
    }

    public function map(callable $callback): Series
    {
        return new Series(array_map($callback, $this->data), $this->index);
    }

    public function sort(bool $ascending = true): Series
    {
        $data = $this->data;
        $index = $this->index;
        array_multisort($data, $ascending ? SORT_ASC : SORT_DESC, $index);
        return new Series($data, $index);
    }

    // ArrayAccess

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

    public function std(): float
    {
        if (empty($this->data)) {
            return 0.0;
        }

        $mean = $this->mean();
        $variance = array_reduce($this->data, function ($carry, $item) use ($mean) {
            return $carry + pow($item - $mean, 2);
        }, 0) / count($this->data);

        return sqrt($variance);
    }

    /**
     * Convert Series to array
     * @return array
     */
    public function toArray(): array
    {
        return $this->data;
    }

    /**
     * Get the index array
     * @return array
     */
    public function getIndex(): array
    {
        return $this->index;
    }
}