<?php

namespace Ssword\DataAnalysis;

use InvalidArgumentException;
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

    /**
     * filters the dataframe.
     * @param callable $predicate the predicate.
     * @return Query a query of a dataframe containing items that satisfied the predicate.
     */
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

    /**
     * selects a set of columns from a dataframe.
     * @param mixed $columns the columns to select.
     * @return Query a query of a dataframe that contains the selected columns.
     */
    public function select($columns): self
    {
        $data = [];
        foreach ($columns as $column) {
            $data[$column] = $this->df->column($column);
        }

        return new self(new DataFrame($data));
    }

    /**
     * apply a function to each column
     * @return self a new query object with the result dataframe.
     */
    public function apply(callable $callback): self
    {
        $newData = [];
        foreach ($this->df->columns() as $name) {
            $column = $this->df->column($name);
            $newData[$name] = $column->map($callback)->toArray();
        }
        return new self(new DataFrame($newData, $this->index));
    }

    /**
     * sort DataFrame by a column
     * @return self a query with the sorted dataframe.
     */
    public function sort(string $column, bool $ascending = true): self
    {
        if (!isset($this->columns[$column])) {
            throw new InvalidArgumentException("Column not found: $column");
        }

        $sortColumn = $this->df->column($column)->toArray();
        $indices = range(0, count($sortColumn) - 1);
        array_multisort($sortColumn, $ascending ? SORT_ASC : SORT_DESC, $indices);

        $newData = [];
        foreach ($this->df->columns() as $name) {
            $series = $this->df->column($name);
            $data = $series->toArray();
            $newData[$name] = array_map(fn($i) => $data[$i], $indices);
        }

        $newIndex = array_map(fn($i) => $this->index[$i], $indices);
        return new self(new DataFrame($newData, $newIndex));
    }

    /**
     * finishes querying.
     * @return DataFrame the finalized dataframe.
     */
    public function finalize(): DataFrame
    {
        return $this->df;
    }
}