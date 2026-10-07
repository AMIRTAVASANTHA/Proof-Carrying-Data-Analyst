import React from "react";

function QuestionBox({
  question,
  setQuestion,
  handleAsk
}) {

  return (

    <div className="question-box">

      <div className="question-icon">
        🤖
      </div>

      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Example: Which category has the highest revenue?"
        rows="3"
      />

      <button
        className="ask-button"
        onClick={handleAsk}
      >
        Ask DataProof
        <span>→</span>
      </button>

    </div>

  );
}

export default QuestionBox;