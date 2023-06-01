import React, { useEffect, useState } from "react";
import UploadService from "../services/upload-files.service";
import GetFilesDataService from "../services/get-files-data.service";
import '../styles/upload-files.css';
import FilesList from "./files-list.component";
import UploadButton from "./upload-button.component";

interface Props {
  fileInfos: any;
  setFileInfos: (param: any) => void;
}

const UploadFiles = ({ fileInfos, setFileInfos }: Props) => {
  const [selectedFiles, setSelectedFiles] = useState<any[]>([]);
  const [message, setMessage] = useState<string[]>([]);
  const [deleteToggle, setDeleteToggle] = useState<boolean>(false);
  const [prevDeleteToggle, setPrevDeleteToggle] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  
  useEffect(() => {
    if (fileInfos.length === 0 || deleteToggle !== prevDeleteToggle) {
      setLoading(true);
      GetFilesDataService.getFiles().then((response) => {
        setFileInfos(response.data);
      });
      setLoading(false);
    }
  }, [deleteToggle]);

  const selectFiles = (event: any) => {
    setSelectedFiles(event.target.files);
  }

  const upload = (idx: number, file: any) => {
    setLoading(true);
    UploadService.upload(file, (event: any) => {})
      .then((response) => {
        setMessage(message => [...message, "Successfully uploaded: " + file.name]);
        return GetFilesDataService.getFiles();
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
      {fileInfos.length > 0 && <FilesList {... {fileInfos, setFileInfos, deleteToggle, setDeleteToggle, setPrevDeleteToggle}} />}
    </div>
  );
}

export default UploadFiles;