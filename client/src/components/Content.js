import React from 'react';
import useRest from '../interface/useRest';
import ProcessContent from './ProcessContent';

const bff = "http://127.0.0.1:8002/";

function Content() {
  const { isLoading, error, data, triggerFetch } = useRest(bff, "GET", null, true);

  const refetchData = () => {
    triggerFetch();
  };

  console.log(data);

  return (
    <>
      {isLoading && <p>Loading...</p>}
      {error && <p>Error: {error.message}</p>}
      {data && <ProcessContent data={data} refetchData={refetchData} />}
    </>
  );
}

export default Content;