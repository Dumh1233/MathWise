import React from "react";
import '../styles/files-list.css';

interface Props {
    fileInfos: any[];
}
const FilesList = ({ fileInfos }: Props) => {
    return (
        <div className="card filesList">
            <div className="card-header">Files List</div>
            <ul className="list-group list-group-flush">
                {fileInfos &&
                    fileInfos.map((file, index) => (
                      <li className="list-group-item" key={index}>
                            <a href={file.url}>{file.name}</a>
                      </li>
                ))}
            </ul>
      </div>
    )
}

export default FilesList;