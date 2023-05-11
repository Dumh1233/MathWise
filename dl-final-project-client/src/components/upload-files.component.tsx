import React, { useEffect, useState } from "react";
import UploadService from "../services/upload-files.service";
import '../styles/upload-files.css';
import FilesList from "./files-list.component";
import Results from "./results.component";
import UploadButton from "./upload-button.component";

const UploadFiles = () => {
  const [selectedFiles, setSelectedFiles] = useState<any[]>([]);
  const [progressInfos, setProgressInfos] = useState<any[]>([]);
  const [message, setMessage] = useState<string[]>([]);
  const [fileInfos, setFileInfos] = useState<any[]>([]);

  useEffect(() => {
    UploadService.getFiles().then((response) => {
      setFileInfos(response.data);
    });
  }, []);

  const selectFiles = (event: any) => {
    setProgressInfos([]);
    setSelectedFiles(event.target.files);
  }

  const upload = (idx: number, file: any, tempProgressInfos: any) => {
    UploadService.upload(file, (event: any) => {
      tempProgressInfos[idx].percentage = Math.round((100 * event.loaded) / event.total);
      setProgressInfos(tempProgressInfos);
    })
      .then((response) => {
        setMessage(message => [...message, "Successfully uploaded: " + file.name]);
        return UploadService.getFiles();
      })
      .then((files) => {
        setFileInfos(files.data);
      })
      .catch((error) => {
        tempProgressInfos[idx].percentage = 0;
        setMessage(message => [...message, "Could not upload: " + file.name + ", " + error.message]);
        setProgressInfos(tempProgressInfos);
      });
  }

  const uploadFiles = () => {
    let _progressInfos = [];

    for (let i = 0; i < selectedFiles.length; i++) {
      _progressInfos.push({ percentage: 0, fileName: selectedFiles[i].name });
    }

    setProgressInfos(_progressInfos);
    setMessage([]);
    
    for (let i = 0; i < selectedFiles.length; i++) {
      upload(i, selectedFiles[i], _progressInfos);
    }
  }

  return (
    <div className="uploadFiles">
      <h4 className="display-4" >Upload some exams to get started!</h4>
      <UploadButton {... { selectFiles, uploadFiles, selectedFiles }} />
      {progressInfos &&
        progressInfos.map((progressInfo, index) => (
          <div className="progressContainer" key={index}>
            <span>{progressInfo.fileName}</span>
            <div className="progress">
              <div
                className="progress-bar progress-bar-info"
                role="progressbar"
                aria-valuenow={progressInfo.percentage}
                aria-valuemin={0}
                aria-valuemax={100}
                style={{ width: progressInfo.percentage + "%" }}
              >
                {progressInfo.percentage}%
              </div>
            </div>
          </div>
        ))}
      {message.length > 0 && (
        <div>
          {message.map((item: string, i) => {
            if (!item.includes("Success")) return <div className="alert alert-danger" role="alert" key={i}>{item}</div>
            else return <></>;
          }
          )}
        </div>
      )}

      {fileInfos.length > 0 && <FilesList {... {fileInfos}} />}
      <Results {... { fileInfos } } />
    </div>
  );
}

export default UploadFiles;