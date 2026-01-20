export interface ChatRequest {
  session_id: string;
  message: string;
}

export interface ChatResponse {
  response: string;
}
