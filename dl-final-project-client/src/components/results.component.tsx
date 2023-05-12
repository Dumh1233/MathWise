import React, { useState } from "react";
import getResultsService from "../services/get-results.service";
import '../styles/results.css';

interface Props {
  fileInfos: any[];
}

const Results = ({ fileInfos }: Props) => {
    const [results, setResults] = useState<any>(null);

    const getResults = () => {
        getResultsService.getAnswer().then((response) => {
          setResults(response.data);
        });
      };

    return (
        <div className="resultsSection">
            {results ? (
              <div>
                <span><b>Results: </b></span>
                <span className={results.message === 'Wrong' ? 'wrong' : 'correct'}>{results.message}</span>
              </div>
            ) : (
              fileInfos && fileInfos.length > 0 && <button onClick={getResults} className={"btn btn-primary"}>Get Results</button>
            )}
        </div>
    )
}

export default Results;