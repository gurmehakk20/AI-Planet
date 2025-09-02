import { useState } from "react";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/uploadfile/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");

      const data = await res.json();
      setText(data.extracted_text || "No text extracted.");
    } catch (err) {
      console.error(err);
      alert("Error uploading file");
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question || !text) {
      alert("Upload a PDF and type a question first!");
      return;
    }

    const formData = new FormData();
    formData.append("question", question);
    formData.append("context", text);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask/", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      console.error(err);
      alert("Error asking question");
    }
  };

  return (
    <div className="p-4 border rounded-lg max-w-lg mx-auto">
      <h2 className="text-xl font-bold mb-2">Upload PDF</h2>
      
      <input type="file" accept="application/pdf" onChange={handleFileChange} />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="ml-2 px-4 py-1 bg-blue-500 text-white rounded"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>

      {text && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Ask a Question</h3>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type your question..."
            className="border px-2 py-1 rounded w-full"
          />
          <button
            onClick={handleAsk}
            className="mt-2 px-4 py-1 bg-green-500 text-white rounded"
          >
            Ask
          </button>

          {answer && (
            <div className="mt-4 p-2 border rounded bg-gray-100">
              <h3 className="font-semibold">Answer:</h3>
              <p>{answer}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default FileUpload;
