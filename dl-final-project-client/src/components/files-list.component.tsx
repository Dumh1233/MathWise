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
                {fileInfos &&
                    fileInfos.map((fileInfo, index) => (
                        <div key={index}>
                            <FileDisplayModal {... {fileInfo}} />
                        </div>
                ))}
            </ul>
      </div>
    )
}

export default FilesList;