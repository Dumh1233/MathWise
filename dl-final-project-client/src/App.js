import React from "react";
import "./App.css";
import Header from './components/header.component.tsx';
import "bootstrap/dist/css/bootstrap.min.css";

import UploadFiles from "./components/upload-files.component";

function App() {
  return (
    <div className="container">
      <div>
        <Header />
      </div>
      <div className="content">
        <UploadFiles />
      </div>
    </div>
  );
}

export default App;
