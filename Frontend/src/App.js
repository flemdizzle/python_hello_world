import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [message, setMessage] = useState('');

    useEffect(() => {
        axios.get('http://localhost:8000')
            .then(response => {
                setMessage(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the data!", error);
            });
    }, []);

    return (
        <div>
            <h1>{message["message"]}</h1>
        </div>
    );
}

export default App;
