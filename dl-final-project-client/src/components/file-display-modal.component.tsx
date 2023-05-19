import React from "react";
import '../styles/file-display.css';

interface Props {
    fileInfo: any;
    index: number;
}

const FileDisplayModal = ({ fileInfo, index }: Props) => {
    return (
        <div className="modal fade" id={`formModal${index}`} tabIndex={-1} role="dialog" aria-labelledby={`formModal${index}Title`} aria-hidden="true">
            <div className="modal-dialog modal-dialog-centered" role="document">
                <div className="modal-content">
                <div className="modal-header">
                    <h5 className="modal-title" id={`formModal${index}Title`}>{fileInfo.name}</h5>
                    <button type="button" className="close" data-bs-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div className="modal-body">
                    <div>
                        {fileInfo.segmentedPages && fileInfo.segmentedPages.map((url:string,key:string)=> (
                            <img 
                                alt="segmented page" 
                                className="img-fluid"
                                src={url} 
                            />
                        ))}
                    </div>
                </div>
                </div>
            </div>
        </div>
    )
}

export default FileDisplayModal;