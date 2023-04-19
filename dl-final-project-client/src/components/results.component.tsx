import React from "react";
import { useState } from "react";
import getResultsService from "../services/get-results.service";

const Results = () => {
    const [results, setResults] = useState<any>(null);
    
    const getResults = () => {
        getResultsService.getAnswer().then((response) => {
          setResults(response.data);
          console.log(response.data)
        });
      };

    return (
        <div>
            <input type="button" onClick={getResults} value="Get Results" />
            {results && results.message && <div>{results.message}</div>}
        </div>
    )
}

export default Results;