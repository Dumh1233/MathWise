import React from "react";
import '../styles/files-list.css';
import FileDisplayModal from "./file-display-modal";
import UploadService from "../services/upload-files.service";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface Props {
    fileInfos: any[];
    deleteToggle: boolean;
    setDeleteToggle: (param: boolean) => void;
}
const FilesList = ({ fileInfos, deleteToggle, setDeleteToggle }: Props) => {
    const handleEmptyServer = () => {
        UploadService.deleteAll().then(() => {
            setDeleteToggle(!deleteToggle);
        })
    }
    return (
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
                                <button type="button"  className="btn btn-primary" data-bs-toggle="modal" data-bs-target={`#ModalCenter${index}`}>
                                    See form
                                </button>
                            </div>
                            <FileDisplayModal {... {fileInfo, index}} />
                        </div>
                ))}
            </ul>
      </div>
    )
}

export default FilesList;