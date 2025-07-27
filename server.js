import express from 'express';
import { spawn } from 'child_process';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Serve static files like bot2.html
app.use(express.static(path.join(__dirname, 'public')));

// POST /classify endpoint
app.post('/classify', (req, res) => {
    const emails = req.body.emails || [];

    const python = spawn('python3', ['classifier1.py']);
    let dataToSend = '';
    let dataToErr = '';

    python.stdout.on('data', (data) => {
        dataToSend += data.toString();
    });

    python.stderr.on('data', (data) => {
        dataToErr += data.toString();
    });

    python.on('close', (code) => {
        if (code !== 0 || dataToErr) {
            return res.status(500).json({ error: dataToErr || 'Error processing request.' });
        }
        try {
            const result = JSON.parse(dataToSend);
            res.json(result);
        } catch (err) {
            res.status(500).json({ error: 'Failed to parse response.' });
        }
    });

    python.stdin.write(JSON.stringify({ emails }));
    python.stdin.end();
});

// Optional: Redirect root URL to bot2.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'bot2.html'));
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
