import React, { useState } from "react";
import "./App.css";
import Header from './components/header.component.tsx';
import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import UploadFiles from "./components/upload-files.component";
import FileResults from "./components/file-results.component";

const App = () => {
  const [fileInfos, setFileInfos] = useState([]);
  return (
    <div className="container">
      <div>
        <Header />
      </div>
      <div className="content">
        <Router>
          <Routes>
            <Route index path="/" element={<UploadFiles {... { fileInfos, setFileInfos }} />} />
            <Route path="/results" element={<FileResults />} />
          </Routes>
        </Router>
      </div>
    </div>
  );
}

export default App;
