import React from "react";
import { useLocation } from 'react-router-dom'
import { useNavigate } from "react-router";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import '../styles/file-results.css';

const FileResults = () => {
    const location = useLocation()
    const { from } = location.state
    const nav = useNavigate();
    console.log(from.segmentedEquations.length);
    console.log(new Set(from.segmentedEquations).size);
    return (
        <>
            <button className="btn btn-primary backButton" type="button" onClick={() => nav(-1)}>
                <FontAwesomeIcon icon={faArrowLeft} />
            </button>
            <h1 className="filename">{from.name.split('.')[0]}</h1>
            <div>
                {from.segmentedEquations && from.segmentedEquations.map((url:string, key:string)=> (
                    <div className="imageContainer" key={key}>
                        <img 
                            alt="segmented page" 
                            className="img-fluid"
                            src={url} 
                        />
                        <br />
                    </div>
                ))}
            </div>
        </>
    )
}

export default FileResults;