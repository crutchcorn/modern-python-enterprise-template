import { HelloWorld } from "components";
import { useEffect, useState } from "react";

function App() {
  const [spec, setSpec] = useState<unknown>(null);

  useEffect(() => {
    fetch("/openapi.json")
      .then((res) => res.json())
      .then(setSpec);
  }, []);

  return (
    <>
      <HelloWorld />
      <pre>{JSON.stringify(spec, null, 2)}</pre>
    </>
  );
}

export default App;
