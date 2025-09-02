import { useState } from "react";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

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

      if (!res.ok) {
        throw new Error("Upload failed");
      }

      const data = await res.json();
      setText(data.extracted_text || "No text extracted.");
    } catch (err) {
      console.error(err);
      alert("Error uploading file");
    } finally {
      setLoading(false);
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
        <div className="mt-4 p-2 border rounded bg-gray-100 max-h-64 overflow-y-auto">
          <h3 className="font-semibold mb-1">Extracted Text:</h3>
          <pre className="whitespace-pre-wrap">{text}</pre>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
