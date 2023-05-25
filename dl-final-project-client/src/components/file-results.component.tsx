import React from "react";
import { useLocation } from 'react-router-dom'
import { useNavigate } from "react-router";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import '../styles/file-results.css';

interface Equation {
    image: string;
    result: string;
}

const FileResults = () => {
    const location = useLocation()
    const { from } = location.state
    const nav = useNavigate();
    return (
        <>
            <button className="btn btn-primary backButton" type="button" onClick={() => nav(-1)}>
                <FontAwesomeIcon icon={faArrowLeft} />
            </button>
            <h1 className="filename">{from.name.split('.')[0]}</h1>
            <div>
                {from.segmentedEquations && from.segmentedEquations.map((equation:Equation, key:string)=> (
                    <div className="imageContainer" key={key}>
                        <img 
                            alt="segmented page" 
                            className="img-fluid"
                            src={equation.image} 
                        />
                        <br />
                    </div>
                ))}
            </div>
        </>
    )
}

export default FileResults;