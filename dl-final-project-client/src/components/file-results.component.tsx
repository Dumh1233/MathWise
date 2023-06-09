import React from "react";
import { useLocation } from 'react-router-dom'
import { useNavigate } from "react-router";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft, faCircleXmark, faCheckCircle } from "@fortawesome/free-solid-svg-icons";
import '../styles/file-results.css';

interface Question {
    image: string;
    parsed: string;
    result: string;
    type: string;
}

interface Props {
    fileInfos: any[];
}

const FileResults = ({ fileInfos }: Props) => {
    const location = useLocation();
    const { filename } = location.state;
    const nav = useNavigate();

    const fileInfo = fileInfos.find((fileInfo) => fileInfo.name === filename);

    return (
        <>
            <button className="btn btn-primary backButton" type="button" onClick={() => nav(-1)}>
                <FontAwesomeIcon icon={faArrowLeft} />
            </button>
            <h1 className="filename">{fileInfo.name.split('.')[0]}</h1>
            <table className="table">
                <thead>
                    <tr>
                        <th scope="col">Detected</th>
                        <th scope="col">Parsed</th>
                        <th scope="col">Result</th>
                    </tr>
                </thead>
                <tbody>
                    {fileInfo.questionsData.map((q:Question, index:number)=> (
                        <tr key={index}>
                            <th scope="row">
                                <img 
                                    alt="segmented page" 
                                    className="img-fluid"
                                    src={q.image} 
                                />
                            </th>
                            <th scope="row">{q.parsed}</th>
                            <th scope="row">
                                {q.result &&  q.result === "Correct" ? <FontAwesomeIcon icon={faCheckCircle} style={{ color: 'green', fontSize: '30px' }}/> : 
                                    (q.result === "Wrong" ? <FontAwesomeIcon icon={faCircleXmark} style={{ color: 'red', fontSize: '30px' }}/> : <span>None</span>)
                                }
                            </th>
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    )
}

export default FileResults;