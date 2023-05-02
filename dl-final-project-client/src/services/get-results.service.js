import http from "../http-common";

class GetResultsService {

  getAnswer() {
    return http.get("/answer");
  }
}

export default new GetResultsService();
