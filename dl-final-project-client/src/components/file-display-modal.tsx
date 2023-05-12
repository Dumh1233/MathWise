import React from "react";
import '../styles/file-display.css';

interface Props {
    fileInfo: any;
}

const FileDisplayModal = ({ fileInfo }: Props) => {
    return (
        <>
            <div className="fileLink">
                <a className="fileName" target="_blank" rel="noopener noreferrer" href={fileInfo.url}>{fileInfo.name}</a>
                <button type="button"  className="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModalCenter">
                    See form
                </button>
            </div>

            <div className="modal fade" id="exampleModalCenter" tabIndex={-1} role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                <div className="modal-dialog modal-dialog-centered" role="document">
                    <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title" id="exampleModalLongTitle">{fileInfo.name}</h5>
                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div className="modal-body">
                        <div className="pageExampleCtr">
                            {fileInfo.segmentedPages && fileInfo.segmentedPages.map((url:string,key:string)=> (
                                <img 
                                    key={key} 
                                    alt="segmented page" 
                                    className="pageExample"
                                    height={300} 
                                    width={200}
                                    src={url} 
                                />
                            ))}
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default FileDisplayModal;