import http from "../http-common";

class GetFilesDataService {
  getFiles() {
    return http.get("/files");
  }

  getForm(filename) {
      return http.get(`/pages/${filename}`)
  }

  getQuestionsData(filename) {
    return http.get(`/questions/${filename}`)
  }
}

export default new GetFilesDataService();
