import { useState, useEffect, useCallback } from 'react';

function useRest(url, method, body = null, autoFetch = false) {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [trigger, setTrigger] = useState(autoFetch); // Automatically fetch data if autoFetch

  const triggerFetch = useCallback(() => setTrigger(true), []);

  useEffect(() => {
    if (!trigger && !autoFetch) return; // Do not fetch if not trigger and autoFetch is not enabled

    const fetchData = async () => {
      setIsLoading(true);
      setError(null); // Reset state before fetching
      try {
        let response;
        if (method !== "GET") {
          response = await fetch(url, {
            method,
            body: JSON.stringify(body),
            headers: { 'Content-Type': 'application/json' },
          });
        } else {
          response = await fetch(url);
        }

        if (!response.ok) throw new Error('Network response was not ok');

        const json = await response.json();
        setData(json);
      } catch (error) {
        setError(error);
      } finally {
        setIsLoading(false);
        setTrigger(false); // Reset trigger
      }
    };

    fetchData();
  }, [url, method, body, trigger, autoFetch]);

  return { isLoading, error, data, triggerFetch };
}

export default useRest;