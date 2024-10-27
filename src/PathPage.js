import React from 'react';
import { useParams } from 'react-router-dom';

const PathPage = () => {
    const { id } = useParams(); 

    return (
        <div>
            <h1>Страница с ID: {id}</h1>
            {/* Здесь можно добавить логику */}
        </div>
    );
};

export default PathPage;
