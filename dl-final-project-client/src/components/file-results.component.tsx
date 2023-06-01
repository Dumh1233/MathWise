import React, { useEffect, useState } from "react";
import { useLocation } from 'react-router-dom'
import { useNavigate } from "react-router";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft, faChevronDown } from "@fortawesome/free-solid-svg-icons";
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

    const [equations, setEquations] = useState<any[]>([]);
    const [shapes, setShapes] = useState<any[]>([]);
    const [shapeMultiples, setShapeMultiples] = useState<any[]>([]);

    type question_types_dict_type = {'equation': (param: any) => void, 'shape': (param: any) => void, 'shapeMultiple': (param: any) => void};
    const QUESTION_TYPES_DICT: question_types_dict_type = {'equation': setEquations, 'shape': setShapes, 'shapeMultiple': setShapeMultiples};

    useEffect(() => {
        Object.keys(QUESTION_TYPES_DICT).forEach((questionType: string) => {
            let questions = fileInfo.questionsData.filter((quesion: any) => quesion.type === questionType);
            QUESTION_TYPES_DICT[questionType as keyof question_types_dict_type](questions);
        })            
    }, []);

    return (
        <>
            <button className="btn btn-primary backButton" type="button" onClick={() => nav(-1)}>
                <FontAwesomeIcon icon={faArrowLeft} />
            </button>
            <h1 className="filename">{fileInfo.name.split('.')[0]}</h1>
            <div className="accordion accordion-flush" id="questionsContainer">
                <div className="accordion-item">
                    <h2 className="accordion-header" id="equationHeading">
                    <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#accordionEquations">
                        Equations ({equations.length})
                        <FontAwesomeIcon icon={faChevronDown}/>
                    </button>
                    </h2>
                    <div id="accordionEquations" className="accordion-collapse collapse" data-bs-parent="#questionsContainer">
                        <div className="accordion-body">
                            {equations &&
                                equations.map((q:Question, index:number)=> (
                                    <div className="questionContainer" key={index}>
                                        <img 
                                            alt="segmented page" 
                                            className="img-fluid"
                                            src={q.image} 
                                        />
                                        <div>{q.parsed}</div>
                                        {q.result ? <div>{q.result}</div> : <div>None</div>}
                                    </div>
                                ))
                            }
                        </div>
                    </div>
                </div>
                <div className="accordion-item">
                    <h2 className="accordion-header" id="shapesHeading">
                    <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#accordionShapes">
                        Shapes ({shapes.length})
                        <FontAwesomeIcon icon={faChevronDown}/>
                    </button>
                    </h2>
                    <div id="accordionShapes" className="accordion-collapse collapse" data-bs-parent="#questionsContainer">
                        <div className="accordion-body">
                            {shapes &&
                                shapes.map((q:Question, index:number)=> (
                                    <div className="questionContainer" key={index}>
                                        <img 
                                            alt="segmented page" 
                                            className="img-fluid"
                                            src={q.image} 
                                        />
                                        <div>{q.parsed}</div>
                                        {q.result ? <div>{q.result}</div> : <div>None</div>}
                                    </div>
                                ))
                            }
                        </div>
                    </div>
                </div>
                <div className="accordion-item">
                    <h2 className="accordion-header" id="shapeMultiplesHeading">
                    <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#accordionShapeMultiples">
                        shapeMultiples ({shapeMultiples.length})
                        <FontAwesomeIcon icon={faChevronDown}/>
                    </button>
                    </h2>
                    <div id="accordionShapeMultiples" className="accordion-collapse collapse" data-bs-parent="#questionsContainer">
                        <div className="accordion-body">
                            {shapeMultiples &&
                                shapeMultiples.map((q:Question, index:number)=> (
                                    <div className="questionContainer" key={index}>
                                        <img 
                                            alt="segmented page" 
                                            className="img-fluid"
                                            src={q.image} 
                                        />
                                        <div>{q.parsed}</div>
                                        {q.result ? <div>{q.result}</div> : <div>None</div>}
                                    </div>
                                ))
                            }
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default FileResults;