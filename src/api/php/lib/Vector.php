<?php

// was going to be a mathematically accurate vector. but
// became numpy like.

namespace Ssword\LinearAlgebra;

use InvalidArgumentException;

/**
 * @param array<int> $items
 * @return \SplFixedArray
 */
function _vector_implementation_toSPLFixedArray(array $items)
{
    $numberOfItems = count($items);
    $spl = new \SplFixedArray($numberOfItems);

    for ($i = 0; $i < $numberOfItems; $i++) {
        $spl[$i] = $items[$i];
    }

    return $spl;
}

class Vector implements \ArrayAccess
{
    /**
     * @var array<int | float>
     */
    public \SplFixedArray $elements;

    /**
     * @var ?array
     */
    private ?array $_shapeCache = null;

    public function __construct(array $elements = [])
    {
        $this->elements = _vector_implementation_toSPLFixedArray($elements);
        $this->_shapeCache = null;
    }

    /**
     * @return array
     */
    public function shape()
    {
        if ($this->_shapeCache === null) {
            $this->_shapeCache = [count($this->elements)];
        }

        return $this->_shapeCache;
    }

    /**
     * @param int|float|Vector $other
     * @return void
     */
    public function add(
        mixed $other
    ): Vector {
        return match (true) {
            is_int($other) || is_float($other) => $this->_addNumeric($other),
            $other instanceof Vector => $this->_addVector($other),
            default => throw new \InvalidArgumentException('Argument must be an integer, float, or Vector.'),
        };
    }

    /**
     * @return Vector
     */
    public function sum()
    {
        $acc = 0;

        foreach ($this->elements as $it) {
            $acc += $it;
        }

        return new self([$acc]);
    }

    public function product()
    {
        $acc = 1;

        foreach ($this->elements as $it) {
            $acc *= $it;
        }

        return new Vector([$acc]);
    }

    public function dot(Vector $other)
    {
        if ($other->shape()[0] !== $this->shape()[0]) {
            throw new InvalidArgumentException("Vectors operand to the dot product must have the same shape.");
        }

        $mag = $this->shape()[0];

        $result = 0;

        for ($i = 0; $i < $mag; $i++) {
            $a_i = $this[$i];
            $b_i = $other[$i];

            $result += ($a_i * $b_i);
        }

        return new Vector([$result]);
    }

    public function sort()
    {
        $elements = iterator_to_array($this->elements);
        sort($elements, SORT_NUMERIC);
        return new Vector($elements);
    }

    public function mean()
    {
        $shape = $this->shape();

        if ($shape[0] === 0) {
            return 0; // avoid 0 division.
        }

        return new Vector([$this->sum()->asFloat() / $shape[0]]);
    }

    public function median()
    {
        $shape = $this->shape();
        $count = $shape[0];

        if ($count === 0) {
            throw new \InvalidArgumentException('Cannot compute median of an empty vector.');
        }

        $sorted = $this->sort();

        $elements = iterator_to_array($sorted->elements);

        if ($count % 2 === 1) {
            // odd number of elements, return the middle one.
            return new Vector([
                $elements[(int) floor($count / 2)]
            ]);
        }

        // even number of elements, return the average of the two middle ones.
        $middleCount = (int) floor($count / 2);

        // this is the item at half of the vector.
        $mid1 = $elements[$middleCount - 1];

        // this is the item at one past half of the vector.
        $mid2 = $elements[$middleCount];

        return new Vector([($mid1 + $mid2) / 2]);
    }

    /**
     * @return Vector
     */
    public function mode()
    {
        $occurrences = [
            // item => count
        ];

        foreach ($this->elements as $item) {
            if (isset($occurrences[$item])) {
                $occurrences[$item]++;
            } else {
                $occurrences[$item] = 1;
            }
        }

        $highestOccurrenceItems = [];
        $highestOccurrence = 0;

        foreach ($occurrences as $item => $count) {
            if ($count > $highestOccurrence) {
                $highestOccurrence = $count;
                $highestOccurrenceItems = [$item];
            } else if ($count === $highestOccurrence) {
                $highestOccurrenceItems[] = $item;
            }
        }

        return new Vector($highestOccurrenceItems);
    }

    /**
     * @param int|float $other
     * @return Vector
     */
    private function _addNumeric(mixed $other)
    {
        $newElements = [];

        foreach ($this->elements as $element) {
            $newElements[] = $element + $other;
        }

        return new Vector($newElements);
    }

    private function _addVector(Vector $other): Vector
    {
        $shape = $this->shape();
        $otherVectorShape = $other->shape();

        if ($shape[0] !== $otherVectorShape[0]) {
            throw new \InvalidArgumentException('Vectors must be of the same length for addition.');
        }

        $newElements = [];

        for ($i = 0; $i < $shape[0]; $i++) {
            $newElements[] = $this->elements[$i] + $other->elements[$i];
        }

        return new Vector($newElements);
    }

    // casts.
    public function asInteger()
    {
        if ($this->shape()[0] !== 1) {
            throw new \LengthException("Vector method `asInteger` expects the vector to have a shape of [1]");
        }

        return (int) floor($this[0]); // truncate the decimal.
    }

    public function asFloat()
    {
        if ($this->shape()[0] !== 1) {
            throw new \LengthException("Vector method `asFloat` expects the vector instance to have a shape of `Vector([1])`");
        }

        return (float) $this[0]; // truncate the decimal.
    }

    public function asArray()
    {
        return $this->elements->toArray();
    }

    // ArrayAccess

    /**
     * @param mixed $offset
     * @throws \LogicException If the index is not an integer.
     * @throws \OutOfBoundsException If the index exceeds the length of the vector.
     * @return float|int
     */
    public function offsetGet(mixed $offset): mixed
    {
        if (!is_int($offset)) {
            throw new \LogicException("Cannot get an element not indexed by an integer.");
        }

        if ($this->shape()[0] < $offset) {
            throw new \OutOfBoundsException("Cannot get an element outside of configured shape.");
        }

        return $this->elements[$offset];
    }

    public function offsetSet(mixed $offset, mixed $value): void
    {
        if ($offset === null) {
            throw new \LogicException("A vector cannot grow in size.");
        }

        if (!is_int($offset)) {
            throw new \LogicException("Cannot set an element not indexed by an integer.");
        }

        if ($this->shape()[0] < $offset) {
            throw new \OutOfBoundsException("Cannot set an element outside of configured shape.");
        }

        $this->elements[$offset] = $value;
    }

    public function offsetUnset(mixed $offset): void
    {
        if (!is_int($offset)) {
            throw new \LogicException("Cannot unset an element not indexed by an integer.");
        }

        if ($this->shape()[0] < $offset) {
            throw new \OutOfBoundsException("Cannot set an element outside of configured shape.");
        }

        unset($this->elements[$offset]);
    }

    public function offsetExists(mixed $offset): bool
    {
        return is_int($offset) && isset($this->elements[$offset]);
    }

    // querying.
    public function where(callable $predicate)
    {
        $satisfiers = [];

        foreach ($this->elements as $it) {
            if ($predicate($it)) {
                $satisfiers[] = $it;
            }
        }

        return new Vector($satisfiers);
    }
}
