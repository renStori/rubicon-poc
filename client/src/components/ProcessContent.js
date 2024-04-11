import React, { useState } from 'react';
import { Button, Heading } from '@chakra-ui/react';
import useRest from '../interface/useRest';

const bff = "http://127.0.0.1:8002/";

function ProcessContent({ data, refetchData }) {
  const { id, name, process, content } = data;

  const [currentAction, setCurrentAction] = useState(null);

  const { isLoading, error, triggerFetch } = useRest(bff + "action", "POST", currentAction);

  const handleClick = (item) => {
    setCurrentAction({
      [item.source]: {
        [id]: {
          [item.context]: item.value,
        },
      },
    });
    triggerFetch();
    refetchData();
  };

  const buildLayout = () => {
    return content.map((item) => {
      if (item.type === "button") {
        const color = ["continue", "true", "contract_signed"].includes(item.value) ? 'green' : item.value === false ? "gray" : "green"
        return (
          <Button colorScheme={color} key={item.value} onClick={() => handleClick(item)}>
            {item.text}
          </Button>
        );
      }
      return null;
    });
  };

  const layout = buildLayout();

  return (
    <>
      {isLoading && <div>Loading...</div>}
      {error && <div>Error: {error.message}</div>}
      {name && <Heading>{name}</Heading>}
      <Heading size='xs' color='tomato' mb={6}>{process}</Heading>
      {layout}
    </>
  );
}

export default ProcessContent;