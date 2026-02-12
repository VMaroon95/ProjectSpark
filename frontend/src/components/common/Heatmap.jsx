function Heatmap({ cells, architectures, subjects }) {
    const getColor = (val) => {
        if (val >= 0.75) return '#2ea043';
        if (val >= 0.70) return '#3fb950';
        if (val >= 0.65) return '#d29922';
        if (val >= 0.60) return '#db6d28';
        return '#f85149';
    };

    const cellMap = {};
    (cells || []).forEach(c => { cellMap[c.architecture + ':' + c.subject] = c.accuracy; });

    return React.createElement('div', { className: 'heatmap-container' },
        React.createElement('table', { className: 'heatmap-table' },
            React.createElement('thead', null,
                React.createElement('tr', null,
                    React.createElement('th', null, ''),
                    ...(subjects || []).map(s =>
                        React.createElement('th', { key: s }, formatters.subjectName(s))
                    )
                )
            ),
            React.createElement('tbody', null,
                ...(architectures || []).map(arch =>
                    React.createElement('tr', { key: arch },
                        React.createElement('td', { className: 'arch-label' }, formatters.archName(arch)),
                        ...(subjects || []).map(subj => {
                            const val = cellMap[arch + ':' + subj] || 0;
                            return React.createElement('td', {
                                key: subj,
                                className: 'heatmap-cell',
                                style: { backgroundColor: getColor(val) + '33', color: getColor(val) },
                            }, formatters.percent(val));
                        })
                    )
                )
            )
        )
    );
}
window.Heatmap = Heatmap;
