function SweepResults() {
    const [results, setResults] = React.useState(null);

    React.useEffect(() => {
        api.getEvalResults().then(setResults).catch(() => {});
    }, []);

    if (!results) return React.createElement('div', { className: 'loading' }, 'Loading results...');

    const archs = Object.entries(results.results);

    return React.createElement('div', { className: 'sweep-results' },
        React.createElement('h2', null, 'Detailed Sweep Results'),
        React.createElement('p', { className: 'subtitle' },
            `${results.metadata.model} — ${results.metadata.benchmark.toUpperCase()} — ${results.metadata.architectures_tested} architectures`
        ),
        React.createElement('table', { className: 'results-table' },
            React.createElement('thead', null,
                React.createElement('tr', null,
                    React.createElement('th', null, 'Architecture'),
                    React.createElement('th', null, 'Overall'),
                    React.createElement('th', null, 'STEM'),
                    React.createElement('th', null, 'Humanities'),
                    React.createElement('th', null, 'Social Sci.'),
                    React.createElement('th', null, 'Other'),
                )
            ),
            React.createElement('tbody', null,
                ...archs.map(([key, data]) =>
                    React.createElement('tr', { key },
                        React.createElement('td', null, formatters.archName(key)),
                        React.createElement('td', { className: 'num' }, formatters.percent(data.overall_accuracy)),
                        React.createElement('td', { className: 'num' }, formatters.percent(data.subjects.stem.accuracy)),
                        React.createElement('td', { className: 'num' }, formatters.percent(data.subjects.humanities.accuracy)),
                        React.createElement('td', { className: 'num' }, formatters.percent(data.subjects.social_sciences.accuracy)),
                        React.createElement('td', { className: 'num' }, formatters.percent(data.subjects.other.accuracy)),
                    )
                )
            )
        ),
    );
}
window.SweepResults = SweepResults;
