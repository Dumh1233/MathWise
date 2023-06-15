import React, { useEffect,useState } from "react";
import { useLocation } from 'react-router-dom'
import { useNavigate } from "react-router";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft, faCircleXmark, faCheckCircle } from "@fortawesome/free-solid-svg-icons";
import '../styles/file-results.css';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import ProgressProvider from "./progress-provider";

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
    const [grade,setGrade] = useState(0);
    const [animGrade,setAnimGrade] = useState(0);
    const [textColor,setTextColor] = useState("#E32636");

    const animateGrade = ()=>{
        let numOfWrongAnswers = 0;
        let numOfCorrectAnswers = 0;
        for(let i = 0; i<fileInfo.questionsData.length;i++){
<<<<<<< Updated upstream
            if(fileInfo.questionsData[i].result == "Wrong"){
                numOfWrongAnswers++;
            }
            if(fileInfo.questionsData[i].result == "Correct"){
=======
            if(fileInfo.questionsData[i].result === "Wrong"){
                numOfWrongAnswers++;
            }
            if(fileInfo.questionsData[i].result === "Correct"){
>>>>>>> Stashed changes
                numOfCorrectAnswers++;
            }
        }
        setGrade(Math.floor((numOfCorrectAnswers / (numOfWrongAnswers + numOfCorrectAnswers)) * 100));
        let thisGrade = 0;
        const interval = setInterval(()=>{
            if(thisGrade < 30){
                setTextColor("#E32636")
            }
            else if(thisGrade >= 30 && thisGrade < 75){
                setTextColor("#FF7F50")
            }
            else if(thisGrade >= 75){
                setTextColor("#32de84")
            }
<<<<<<< Updated upstream
            if(thisGrade != Math.floor((numOfCorrectAnswers / (numOfWrongAnswers + numOfCorrectAnswers)) * 100)){
=======
            if(thisGrade !== Math.floor((numOfCorrectAnswers / (numOfWrongAnswers + numOfCorrectAnswers)) * 100)){
>>>>>>> Stashed changes
                thisGrade++;
                setAnimGrade(thisGrade);
            }
            else{
                clearInterval(interval);
            }
        }, (2.5/Math.floor((numOfCorrectAnswers / (numOfWrongAnswers + numOfCorrectAnswers)) * 100)) * 1000)
    }

    useEffect(()=>{
        setGrade(0);
        setAnimGrade(0);
        setTimeout(() => {
            animateGrade();
        }, 30);
    },[fileInfo])

    return (
        <>
            <button className="btn btn-primary backButton" type="button" onClick={() => nav(-1)}>
                <FontAwesomeIcon icon={faArrowLeft} />
            </button>
            <div style={{width:200, margin:"auto"}}>
            <h3>Final Score:</h3>
            <ProgressProvider valueStart={0} valueNow={animGrade} valueEnd={grade} color={textColor}>
                {(state: any) => <CircularProgressbar value={state.valueEnd} maxValue={100} text={`${state.valueNow}%`} styles={buildStyles({
                    rotation: 0,
                    strokeLinecap: 'round',
                    textSize: '24px',
                    pathTransitionDuration: 3,
                    pathColor: state.color,
                    textColor: state.color,
                    trailColor: '#d6d6d6',
                    backgroundColor: '#3e98c7',
                })} />}
            </ProgressProvider>
            </div>
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