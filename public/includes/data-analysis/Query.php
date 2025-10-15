<?php

namespace Ssword\DataAnalysis;

/**
 * In memory querying for DataFrame.
 */
class Query
{
    private DataFrame $df;
    private array $index;

    public function __construct(DataFrame $df)
    {
        $this->df = $df;
        $this->index = $df->index();
    }

    public function where(callable $predicate): self
    {
        // initialize indexes and new data array.
        $data = [];
        $newIndex = [];

        foreach ($this->df->columns() as $col) {
            $data[$col] = [];
        }

        foreach ($this->index as $idx) {
            $row = $this->df->row($idx);
            if ($predicate($row)) {
                foreach ($this->df->columns() as $col) {
                    $data[$col][] = $this->df[$col][$idx];
                }
                $newIndex[] = $idx;
            }
        }

        return new self(new DataFrame($data, $newIndex));
    }

    public function select($columns)
    {
        $data = [];
        foreach ($columns as $column) {
            $data[$column] = $this->df->column($column);
        }

        return new self(new DataFrame($data));
    }

    public function finalize(): DataFrame
    {
        return $this->df;
    }
}