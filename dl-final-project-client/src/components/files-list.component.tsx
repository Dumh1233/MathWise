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
                            <a className="fileName" target="_blank" rel="noopener noreferrer" href={file.url}>{file.name}</a>
                            <div className="pageExampleCtr">
                                {file.segmentedPages &&
                                    file.segmentedPages.map((url:string,key:string)=> (<img alt="segmented page" key={key} className="pageExample" height={300} width={200} src={url} />))}
                            </div>
                      </li>
                ))}
            </ul>
      </div>
    )
}

export default FilesList;