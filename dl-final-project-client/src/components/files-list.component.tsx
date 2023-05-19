import React from "react";
import '../styles/files-list.css';
import FileDisplayModal from "./file-display-modal.component";
import UploadService from "../services/upload-files.service";
import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "react-router-dom";


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
                                <div className="actionButtons">
                                    <button type="button"  className="btn btn-primary" data-bs-toggle="modal" data-bs-target={`#formModal${index}`}>
                                        See form
                                    </button>
                                    <Link to="/results" state={{ from: fileInfo }}>
                                        <button type="button" className="btn btn-success">
                                            See Results
                                        </button>
                                    </Link>
                                </div>
                            </div>
                            <FileDisplayModal {... {fileInfo, index}} />
                        </div>
                ))}
            </ul>
      </div>
    )
}

export default FilesList;