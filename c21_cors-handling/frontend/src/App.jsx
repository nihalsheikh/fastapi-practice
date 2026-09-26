import { useState, useEffect } from "react";

const App = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((response) => response.json())
      .then((json) => setData(json))
      .catch((err) => console.error("Error fetching backend data:", err));
  }, []);

  return (
    <div className="bg-zinc-800 w-full h-full flex flex-col justify-center items-center">
      <h1 className="text-4xl text-red-500 items-center justify-center">
        React Frontend with FastAPI Backend
      </h1>
      <p className="text-md text-zinc-400">
        This is CORS handling with 2 differnet source origins
      </p>

      <div className="text-zinc-200 mt-50 flex flex-col justify-center items-center">
        <h1 className="text-2xl">Backend API Data</h1>
        <p>{data ? `Message: ${data.msg}` : "Loading..."}</p>
      </div>
    </div>
  );
};

export default App;
