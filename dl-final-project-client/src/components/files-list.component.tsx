import React, { useState } from "react";
import '../styles/files-list.css';
import FileDisplayModal from "./file-display-modal.component";
import UploadService from "../services/upload-files.service";
import getFilesDataService from "../services/get-files-data.service";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useNavigate } from 'react-router-dom';

interface Props {
    fileInfos: any[];
    setFileInfos: (param: any) => void;
    deleteToggle: boolean;
    setDeleteToggle: (param: boolean) => void;
    setPrevDeleteToggle: (param: boolean) => void;
}
const FilesList = ({ fileInfos, setFileInfos, deleteToggle, setDeleteToggle, setPrevDeleteToggle }: Props) => {
    const navigate = useNavigate();

    const [loadingForm, setLoadingForm] = useState<boolean>(false);
    const [loadingQuestionsData, setLoadingQuestionsData] = useState<boolean>(false);
    const [pages, setPages] = useState<any[]>([])

    const handleEmptyServer = () => {
        UploadService.deleteAll().then(() => {
            setPrevDeleteToggle(deleteToggle)
            setDeleteToggle(!deleteToggle);
        })
    }

    const handleLoadPages = (filename: string) => {
        const currentFile = fileInfos.find((file) => file.name === filename);
        if ('pages' in currentFile) {
            setPages(currentFile.pages);
        } else {
            setLoadingForm(true);
            getFilesDataService.getForm(filename).then((response) => {
                setLoadingForm(false);
                setFileInfos((fileInfos: any) => {
                    return fileInfos.map((fileInfo: any) => {
                      if (fileInfo.name === filename) {
                        return { ...fileInfo, pages: response.data.pages };
                      }
                      return fileInfo; 
                    });
                  });
                setPages(response.data.pages);
            })
        }
    }

    const handleLoadQuestions = (filename: string) => {
        const currentFile = fileInfos.find((file) => file.name === filename);
        if (!('questionsData' in currentFile)) {
            setLoadingQuestionsData(true);
            getFilesDataService.getQuestionsData(filename).then((response) => {
                setFileInfos((fileInfos: any) => {
                    return fileInfos.map((fileInfo: any) => {
                      if (fileInfo.name === filename) {
                        return { ...fileInfo, questionsData: response.data.questions_data };
                      }
                      return fileInfo; 
                    });
                });
                setLoadingQuestionsData(true);
                navigate('/results', {
                    state: {filename: currentFile.name}
                });
            })
        }
    }

    return (
        <>
            {loadingForm && <div className="spinner-border text-primary" role="status" />}
            {loadingQuestionsData && <div className="spinner-border text-primary" role="status" />}
            <div className="card filesList">
                <div className="fileListHeader">
                    <div className="card-header">Files List</div>
                    {fileInfos.length > 0 && <button
                        onClick={handleEmptyServer}
                        className="btn btn-outline-danger deleteButton"
                    >
                        <FontAwesomeIcon icon={faTrash}/>
                    </button>}
                </div>
                <ul className="list-group list-group-flush">
                    {fileInfos.map((fileInfo, index) => (
                            <div key={index}>
                                <div className="fileLink">
                                    <a className="fileName" target="_blank" rel="noopener noreferrer" href={fileInfo.url}>{fileInfo.name}</a>
                                    <div className="actionButtons">
                                        <button 
                                            type="button"
                                            className="btn btn-primary"
                                            data-bs-toggle="modal"
                                            data-bs-target={`#formModal${index}`}
                                            onClick={() => handleLoadPages(fileInfo.name)}>
                                            See form
                                        </button>
                                        {/* <Link to="/results" state={{ from: fileInfo }}> */}
                                        <button
                                            type="button"
                                            className="btn btn-success"
                                            onClick={() => handleLoadQuestions(fileInfo.name)}>
                                            See Results
                                        </button>
                                        {/* </Link> */}
                                    </div>
                                </div>
                                <FileDisplayModal {... {fileInfo, index, pages, loadingForm}} />
                            </div>
                    ))}
                </ul>
            </div>
        </>
    )
}

export default FilesList;