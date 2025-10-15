<?php

namespace Ssword\DataAnalysis;

use InvalidArgumentException;
use Iterator;
use ArrayAccess;
use Countable;
use JsonSerializable;

// Data analysis DataFrame
class DataFrame implements ArrayAccess, Iterator, Countable, JsonSerializable
{
    /** @var array<string,Series> */
    private array $columns;

    /** @var array */
    private array $index;

    /** @var int */
    private int $position = 0;

    /**
     * Create a new DataFrame
     * @param array<string,array> $data column name => column data pairs
     * @param array|null $index optional custom row labels
     */
    public function __construct(array $data = [], ?array $index = null)
    {
        // validate all columns have same length
        // because we should expect a rectangular table
        // not an irregular table. also ensure each column is
        // either an array or a Series so count() is safe.
        $lengths = [];
        foreach ($data as $name => $values) {
            if ($values instanceof Series) {
                $lengths[] = $values->count();
            } elseif (is_array($values)) {
                $lengths[] = count($values);
            } else {
                $type = gettype($values);
                throw new InvalidArgumentException("Column '$name' must be an array or Series, $type given");
            }
        }

        if (!empty($lengths) && count(array_unique($lengths)) > 1) {
            throw new InvalidArgumentException("All columns must have the same length");
        }

        // create a Series for each column
        $this->columns = [];
        foreach ($data as $name => $values) {
            $this->columns[$name] = $values instanceof Series ? $values : new Series($values, $index);
        }

        // set index
        $rowCount = empty($data) ? 0 : count(reset($data));
        $this->index = $index ?? range(0, max(0, $rowCount - 1));
    }

    /**
     * get a column as a Series
     */
    public function column(string $name): Series
    {
        if (!isset($this->columns[$name])) {
            throw new InvalidArgumentException("Column not found: $name");
        }
        return $this->columns[$name];
    }

    /**
     * get a row as a Series
     */
    public function row(mixed $index): Series
    {
        $data = [];
        foreach ($this->columns as $name => $column) {
            $data[$name] = $column[$index];
        }
        return new Series($data, array_keys($this->columns));
    }

    /**
     * get column names
     * @return array<string>
     */
    public function columns(): array
    {
        return array_keys($this->columns);
    }

    /**
     * get an entire row as a series.
     * @return array<string, Series>
     */
    public function rows(): array
    {
        $sampleKey = array_key_first($this->columns);
        $numberOfRows = count($this->columns[$sampleKey]);
        $rows = [];

        for ($i = 0; $i < $numberOfRows; $i++) {
            $rows[] = $this->row($i);
        }

        return $rows;
    }

    /**
     * get row labels
     */
    public function index(): array
    {
        return $this->index;
    }

    /**
     * gdd a new column
     */
    public function addColumn(string $name, Series|array $data): void
    {
        if (is_array($data)) {
            $data = new Series($data, $this->index);
        }

        if ($data->count() !== count($this->index)) {
            throw new InvalidArgumentException("Column length must match DataFrame length");
        }

        $this->columns[$name] = $data;
    }

    /**
     * remove a column
     */
    public function dropColumn(string $name): void
    {
        if (!isset($this->columns[$name])) {
            throw new InvalidArgumentException("Column not found: $name");
        }
        unset($this->columns[$name]);
    }

    /**
     * gets the average of a column in the dataframe.
     * @param mixed $column
     * @return float
     */
    public function mean($column)
    {
        return $this->column($column)->mean();
    }

    /**
     * gets the median of of a column in a dataframe.
     * @param mixed $column
     * @return float
     */
    public function median($column)
    {
        return $this->column($column)->median();
    }

    /**
     * gets the mode of a column in a dataframe
     * @param mixed $column
     */
    public function mode($column)
    {
        return $this->column($column)->mode();
    }

    /**
     * gets the first n rows
     */
    public function head(int $n = 5): self
    {
        $newData = [];
        foreach ($this->columns as $name => $column) {
            $newData[$name] = array_slice($column->toArray(), 0, $n);
        }
        return new self($newData, array_slice($this->index, 0, $n));
    }

    /**
     * gets the last n rows
     */
    public function tail(int $n = 5): self
    {
        $newData = [];
        foreach ($this->columns as $name => $column) {
            $newData[$name] = array_slice($column->toArray(), -$n);
        }
        return new self($newData, array_slice($this->index, -$n));
    }

    // ArrayAccess

    /**
     * implements `isset` for this dataframe.
     */
    public function offsetExists(mixed $offset): bool
    {
        return isset($this->columns[$offset]);
    }

    /**
     * implements array index access for this dataframe.
     * @param mixed $offset the index.
     * @return Series a series containing the data for the column.
     */
    public function offsetGet(mixed $offset): Series
    {
        return $this->column($offset);
    }

    /**
     * implements the index set operation for this dataframe.
     * @param mixed $offset the index
     * @param mixed $value the value to set for this index.
     * @throws \InvalidArgumentException
     * @return void
     */
    public function offsetSet(mixed $offset, mixed $value): void
    {
        if ($offset === null) {
            throw new InvalidArgumentException("Column name must be specified");
        }
        $this->addColumn($offset, $value);
    }

    /**
     * implements the unset(...) operator for this dataframe.
     * @param mixed $offset the index.
     * @return void
     */
    public function offsetUnset(mixed $offset): void
    {
        $this->dropColumn($offset);
    }

    // Iterator Implementation

    /**
     * gets the current element of the iterator.
     * which in this case is the next row.
     * @return Series
     */
    public function current(): Series
    {
        return $this->row($this->index[$this->position]);
    }

    /**
     * returns the key for the current element of the iterator.
     * which in thi case is the key for the next row.
     * @return mixed
     */
    public function key(): mixed
    {
        return $this->index[$this->position];
    }

    /**
     * advances the pointer of the iterator.
     * which in this case will advance the pointer to the
     * next row.
     * @return void
     */
    public function next(): void
    {
        $this->position++;
    }

    /**
     * resets the iterator.
     * @return void
     */
    public function rewind(): void
    {
        $this->position = 0;
    }

    /**
     * checks if the current position is valid. if this returns
     * false then the iterator rewinds.
     * @return bool
     */
    public function valid(): bool
    {
        return isset($this->index[$this->position]);
    }

    // Countable

    // gets how many items / entries are in the dataframe.
    public function count(): int
    {
        return count($this->index);
    }

    // querying
    // query exposes sql-like methods for data analysis such as selecting, and filtering.
    public function query()
    {
        return new Query($this);
    }


    // string coercion.
    // coerce into html string that represents
    // the dataframe.

    /**
     * returns a table representing this DataFrame.
     * @return string
     */
    public function __tostring()
    {
        $s = '<table class="dataframe-table">';

        $s .= '<thead class="dataframe-table-heading>';

        $s .= '<tr class="dataframe-table-column-names>';

        foreach ($this->columns() as $col) {
            $s .= "<th class=\"dataframe-table-column-name\">$col</th>";
        }

        $s .= '</tr>';

        $s .= '</thead>';

        $s .= '<tbody>';

        $numberOfRows = $this->count();

        for ($row = 0; $row < $numberOfRows; $row++) {
            $s .= '<tr class="dataframe-table-row">';

            $rowData = $this->row($row);

            foreach ($rowData as $data) {
                $s .= "<td class=\"dataframe-table-column-data-cell\">$data</td>";
            }

            $s .= "</tr>";
        }

        $s .= "</tbody>";
        $s .= "</table>";

        return $s;
    }

    /**
     * implements JsonSerializable so json_encode($dataFrame) returns rows array.
     * returns an array of rows; each row is an associative array column => value.
     * so returns an array of json objects.
     * @return array<int, array<string,mixed>>
     */
    public function jsonSerialize(): mixed
    {
        $rows = [];
        $numberOfRows = $this->count();
        $colNames = $this->columns();

        for ($r = 0; $r < $numberOfRows; $r++) {
            $row = [];
            foreach ($colNames as $col) {
                $row[$col] = $this->columns[$col][$r];
            }
            $rows[] = $row;
        }

        return $rows;
    }

    // Helper Methods

    private function isNumericColumn(Series $column): bool
    {
        foreach ($column as $value) {
            if (!is_numeric($value)) {
                return false;
            }
        }
        return true;
    }
}
