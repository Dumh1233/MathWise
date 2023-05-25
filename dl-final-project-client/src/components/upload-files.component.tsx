import React, { useEffect, useState } from "react";
import UploadService from "../services/upload-files.service";
import '../styles/upload-files.css';
import FilesList from "./files-list.component";
import Results from "./results.component";
import UploadButton from "./upload-button.component";

const UploadFiles = () => {
  const [selectedFiles, setSelectedFiles] = useState<any[]>([]);
  const [message, setMessage] = useState<string[]>([]);
  const [fileInfos, setFileInfos] = useState<any[]>([]);
  const [deleteToggle, setDeleteToggle] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    UploadService.getFiles().then((response) => {
      console.log(response)
      setFileInfos(response.data);
    });
  }, [deleteToggle]);

  const selectFiles = (event: any) => {
    setSelectedFiles(event.target.files);
  }

  const upload = (idx: number, file: any) => {
    setLoading(true);
    UploadService.upload(file, (event: any) => {})
      .then((response) => {
        setMessage(message => [...message, "Successfully uploaded: " + file.name]);
        return UploadService.getFiles();
      })
      .then((files) => {
        setFileInfos(files.data);
        setLoading(false);
      })
      .catch((error) => {
        setMessage(message => [...message, "Could not upload: " + file.name + ", " + error.message]);
      });
  }

  const uploadFiles = () => {

    setMessage([]);
    
    for (let i = 0; i < selectedFiles.length; i++) {
      upload(i, selectedFiles[i]);
    }
  }

  return (
    <div className="uploadFiles">
      {loading && <div className="spinner-border text-primary" role="status" />}
      <h4 className="display-4" >Upload some exams to get started!</h4>
      <UploadButton {... { selectFiles, uploadFiles, selectedFiles }} />
      {message.length > 0 && (
        <div>
          {message.map((item: string, i) => {
            if (!item.includes("Success")) return <div className="alert alert-danger" role="alert" key={i}>{item}</div>
            else return <></>;
          }
          )}
        </div>
      )}
      {fileInfos.length > 0 && <FilesList {... {fileInfos, deleteToggle, setDeleteToggle}} />}
      <Results {... { fileInfos } } />
    </div>
  );
}

export default UploadFiles;