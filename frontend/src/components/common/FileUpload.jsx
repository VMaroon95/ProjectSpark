function FileUpload({ onFile, accept, label }) {
    const [dragging, setDragging] = React.useState(false);
    const [fileName, setFileName] = React.useState(null);
    const inputRef = React.useRef();

    const handleDrop = (e) => {
        e.preventDefault();
        setDragging(false);
        const file = e.dataTransfer.files[0];
        if (file) { setFileName(file.name); onFile(file); }
    };

    const handleChange = (e) => {
        const file = e.target.files[0];
        if (file) { setFileName(file.name); onFile(file); }
    };

    return React.createElement('div', {
        className: 'file-upload' + (dragging ? ' dragging' : ''),
        onDragOver: (e) => { e.preventDefault(); setDragging(true); },
        onDragLeave: () => setDragging(false),
        onDrop: handleDrop,
        onClick: () => inputRef.current.click(),
    },
        React.createElement('input', {
            ref: inputRef, type: 'file', accept: accept || '.csv',
            onChange: handleChange, style: { display: 'none' },
        }),
        React.createElement('div', { className: 'upload-icon' }, '📁'),
        React.createElement('p', null, fileName || (label || 'Drop a file here or click to browse')),
    );
}
window.FileUpload = FileUpload;
