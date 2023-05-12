import React from 'react';

const EmailControls = ({
  changeIndex,
  currentIndex,
  emailsLength,
  buttonTexts,
  changeFunc,
}) => (
  <>
    <button
      onClick={() => changeIndex(currentIndex, emailsLength, changeFunc, -1)}
      disabled={currentIndex === 0}
    >
      {buttonTexts.previous}
    </button>
    <button
      onClick={() => changeIndex(currentIndex, emailsLength, changeFunc, 1)}
      disabled={currentIndex === emailsLength - 1}
    >
      {buttonTexts.next}
    </button>
  </>
);

export default EmailControls;
