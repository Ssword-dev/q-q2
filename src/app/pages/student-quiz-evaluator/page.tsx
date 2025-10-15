import { useState, FormEvent, ChangeEvent } from "react";

// ✅ Interfaces
interface StudentRecord {
  name: string;
  score: string;
}

type Phase = "get-number-of-students" | "get-records" | "evaluate";

// ✅ Component
export default function App() {
  const [phase, setPhase] = useState<Phase>("get-number-of-students");
  const [numStudents, setNumStudents] = useState<number>(0);
  const [records, setRecords] = useState<StudentRecord[]>([]);

  const handleNumberSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (numStudents > 0) {
      setRecords(
        Array.from({ length: numStudents }, () => ({ name: "", score: "" }))
      );
      setPhase("get-records");
    }
  };

  const handleRecordsChange = (
    index: number,
    field: keyof StudentRecord,
    value: string
  ) => {
    setRecords(prev => {
      const copy = [...prev];
      copy[index][field] = value;
      return copy;
    });
  };

  const handleRecordsSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setPhase("evaluate");
  };

  const average: number =
    records.length > 0
      ? records.reduce((acc, cur) => acc + Number(cur.score || 0), 0) /
        records.length
      : 0;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
      <div className="bg-white rounded-2xl shadow-lg p-6 w-full max-w-md">
        {phase === "get-number-of-students" && (
          <form onSubmit={handleNumberSubmit} className="flex flex-col gap-4">
            <div>
              <label
                htmlFor="num"
                className="block text-gray-700 font-medium mb-1"
              >
                Enter the number of students:
              </label>
              <input
                type="number"
                id="num"
                value={numStudents}
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  setNumStudents(Number(e.target.value))
                }
                className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring focus:ring-blue-200"
                required
                min={1}
              />
            </div>
            <button
              type="submit"
              className="mt-2 w-full bg-blue-600 hover:bg-blue-700 text-white rounded-md py-2 font-semibold shadow transition"
            >
              Submit
            </button>
          </form>
        )}

        {phase === "get-records" && (
          <form onSubmit={handleRecordsSubmit} className="flex flex-col gap-4">
            {records.map((student, i) => (
              <div key={i} className="bg-gray-50 p-3 rounded-lg shadow-inner">
                <div className="mb-2">
                  <label
                    htmlFor={`student-${i}-name`}
                    className="block text-gray-700 font-medium mb-1"
                  >
                    Student {i + 1} Name:
                  </label>
                  <input
                    type="text"
                    id={`student-${i}-name`}
                    value={student.name}
                    onChange={(e: ChangeEvent<HTMLInputElement>) =>
                      handleRecordsChange(i, "name", e.target.value)
                    }
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring focus:ring-blue-200"
                    required
                  />
                </div>

                <div>
                  <label
                    htmlFor={`student-${i}-score`}
                    className="block text-gray-700 font-medium mb-1"
                  >
                    Score:
                  </label>
                  <input
                    type="number"
                    id={`student-${i}-score`}
                    value={student.score}
                    onChange={(e: ChangeEvent<HTMLInputElement>) =>
                      handleRecordsChange(i, "score", e.target.value)
                    }
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring focus:ring-blue-200"
                    required
                  />
                </div>
              </div>
            ))}

            <button
              type="submit"
              className="mt-2 w-full bg-green-600 hover:bg-green-700 text-white rounded-md py-2 font-semibold shadow transition"
            >
              Evaluate
            </button>
          </form>
        )}

        {phase === "evaluate" && (
          <div className="flex flex-col gap-4">
            <h2 className="text-xl font-bold text-gray-800 text-center">
              Evaluation Summary
            </h2>
            <ul className="divide-y divide-gray-200">
              {records.map((r, i) => (
                <li key={i} className="py-2">
                  <span className="font-medium">{r.name}</span> — {r.score}
                </li>
              ))}
            </ul>
            <p className="mt-4 text-lg font-semibold text-center text-gray-700">
              Average Score:{" "}
              <span className="text-blue-600">{average.toFixed(2)}</span>
            </p>
            <button
              onClick={() => setPhase("get-number-of-students")}
              className="mt-4 w-full bg-blue-500 hover:bg-blue-600 text-white rounded-md py-2 font-semibold shadow transition"
            >
              Restart
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
