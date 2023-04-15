import React, { useEffect, useRef, useState } from "react";

interface Props {
    selectFiles: (param: any) => void;
    uploadFiles: () => void;
    selectedFiles: any[];
}
const UploadButton = ({selectFiles, uploadFiles, selectedFiles}: Props) => {
  const [uploadedFileNames, setUploadedFileNames] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const [enableUpload, setEnableUpload] = useState<boolean>(false);

  useEffect(() => {
    selectedFiles.length > 0 ? setEnableUpload(true) : setEnableUpload(false);
  }, [selectedFiles]);

  const handleFileChoice = () => {
    inputRef.current?.click();
  };

  const handleDisplayFileDetails = () => {
    if (inputRef.current && inputRef.current.files) {
      for (let index = 0; index < inputRef.current.files.length; index++) {
        const fileName = inputRef.current.files.item(index)!.name;
        setUploadedFileNames(uploadedFileNames => [...uploadedFileNames, fileName]);
      }        
    }
  };

  const handleChange = (event: any) => {
    selectFiles(event);
    handleDisplayFileDetails();
  };

  const handleUpload = () => {
    setUploadedFileNames([]);
    uploadFiles();
  }

  return (
    <div className="uploadButton">
        <div>
            <input
                ref={inputRef}
                multiple
                onChange={handleChange}
                className="d-none"
                type="file"
            />
            <button
                onClick={handleFileChoice}
                className={`btn btn-outline-${
                uploadedFileNames.length > 0 ? "success" : "primary"
                }`}
            >
              {uploadedFileNames.length > 0 ? `${uploadedFileNames.length} files chosen` : "Choose Files"}
            </button>
        </div>
        {enableUpload && (
            <div>
                <button
                    className="btn btn-success btn-sm"
                    disabled={!selectedFiles}
                    onClick={handleUpload}
                >
                    Upload
                </button>
            </div>
        )}
    </div>
  );
}

export default UploadButton;