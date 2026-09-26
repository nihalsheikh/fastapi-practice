import { useState, useEffect } from "react";

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((res) => res.json())
      .then((json) => setData(json))
      .catch((err) => console.error("Error fetching backend data:", err));
  }, []);

  return (
    <div className="flex flex-col justify-center items-center">
      <h1 className="text-red-500 text-4xl">React with FastAPI</h1>
      <p className="text-md text-zinc-300">
        Connecting backend with frontend avoiding CORS Error and using Env Var
        in backend
      </p>

      <div className="flex flex-col mt-50 justify-center items-center">
        <h1 className="text-sky-500 text-2xl">Backend Data</h1>
        <p className="text-md text-zinc-100">
          {data ? `Message: ${data.message}` : "Loading..."}
        </p>
      </div>
    </div>
  );
};

export default App;
