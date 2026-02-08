const fs = require('fs');
const path = require('path');
const {
    Document,
    Packer,
    Paragraph,
    TextRun,
    HeadingLevel,
    ImageRun,
    AlignmentType,
    Indent,
    LevelFormat,
    TableOfContents,
    Header,
    Footer,
    PageNumber,
    PageOrientation,
    convertInchesToTwip
} = require('docx');

// Configuration
const SOURCE_FILE = path.join(__dirname, '../master_report/20260118_Master_WhitePaper_Final.md');
const OUTPUT_FILE = path.join(__dirname, '../master_report/20260118_Master_WhitePaper_Final_v2.docx');
const IMAGE_DIR = path.join(__dirname, '../master_report');

// Helper to read file safely
function readFile(filePath) {
    try {
        return fs.readFileSync(filePath, 'utf8');
    } catch (error) {
        console.error(`Error reading file ${filePath}:`, error);
        process.exit(1);
    }
}

// Helper to determine image type from extension
function getImageType(imagePath) {
    const ext = path.extname(imagePath).toLowerCase().replace('.', '');
    // docx library expects specific strings
    switch (ext) {
        case 'png': return 'png';
        case 'jpg':
        case 'jpeg': return 'jpeg';
        case 'gif': return 'gif';
        case 'bmp': return 'bmp';
        case 'svg': return 'svg';
        default: return 'png'; // Fallback
    }
}

// Main parsing and generation logic
async function generateDocx() {
    console.log(`Reading source file: ${SOURCE_FILE}`);
    const content = readFile(SOURCE_FILE);
    const lines = content.split(/\r?\n/);

    const children = [];

    // Add Table of Contents
    children.push(new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Table of Contents")]
    }));

    children.push(new TableOfContents("Summary", {
        hyperlink: true,
        headingStyleRange: "1-3",
    }));

    // Page Break after TOC
    children.push(new Paragraph({
        pageBreakBefore: false, // Don't force break immediately, let flow
        children: [] // Just empty paragraph to separate
    }));
    // Actually, a page break is better inserted as a child of a paragraph
    children.push(new Paragraph({
        children: [new TextRun({ break: 1, type: 'page' })]
    }));


    let inList = false;
    let listType = null; // 'bullet' or 'number'

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();

        if (!line) {
            inList = false;
            continue; // Skip empty lines
        }

        // --- Headers ---
        if (line.startsWith('#')) {
            const level = line.match(/^#+/)[0].length;
            const text = line.replace(/^#+\s*/, '').trim();

            let headingLevel;
            // Map markdown levels to docx HeadingLevels
            switch (level) {
                case 1: headingLevel = HeadingLevel.TITLE; break; // Use Title for H1
                case 2: headingLevel = HeadingLevel.HEADING_1; break;
                case 3: headingLevel = HeadingLevel.HEADING_2; break;
                case 4: headingLevel = HeadingLevel.HEADING_3; break;
                case 5: headingLevel = HeadingLevel.HEADING_4; break;
                default: headingLevel = HeadingLevel.HEADING_5;
            }

            // Special handling: formatting in headers? (e.g. **bold**)
            // Simple approach: clean the text for headers or parse it. 
            // For robust parsing, we'd need a full inline parser. 
            // For this task, strict header text extraction is usually safer for TOC.

            // Remove markdown bold/italic markers for the Heading TextRun
            const cleanText = text.replace(/\*\*/g, '').replace(/\*/g, '');

            children.push(new Paragraph({
                heading: headingLevel,
                children: [new TextRun(cleanText)],
                spacing: { before: 240, after: 120 }
            }));
            inList = false;
            continue;
        }

        // --- Images ---
        // Markdown image: ![alt](path)
        const imgMatch = line.match(/^!\[(.*?)\]\((.*?)\)/);
        if (imgMatch) {
            const altText = imgMatch[1];
            let imgPath = imgMatch[2];

            // Resolve path relative to master_report
            // If path starts with figures/, it's relative to master_report root
            const absoluteImgPath = path.resolve(IMAGE_DIR, imgPath);

            if (fs.existsSync(absoluteImgPath)) {
                try {
                    const imgData = fs.readFileSync(absoluteImgPath);
                    const dimensions = { width: 600, height: 400 }; // Default sizing, can be improved with image-size lib if needed, but docx scales reasonably

                    children.push(new Paragraph({
                        alignment: AlignmentType.CENTER,
                        children: [
                            new ImageRun({
                                data: imgData,
                                transformation: {
                                    width: 500, // Standard width for document
                                    height: 300 // Aspect ratio assumption, docx-js requires explicit size
                                },
                                type: getImageType(absoluteImgPath),
                                altText: {
                                    title: altText,
                                    description: altText,
                                    name: path.basename(absoluteImgPath)
                                }
                            }),
                            new TextRun({
                                text: `\n${altText}`, // Caption below image
                                italics: true,
                                size: 20 // 10pt
                            })
                        ],
                        spacing: { before: 240, after: 240 }
                    }));
                } catch (e) {
                    console.warn(`Failed to embed image ${absoluteImgPath}: ${e.message}`);
                    children.push(new Paragraph({
                        children: [new TextRun({ text: `[Image Missing: ${altText}]`, color: "FF0000" })]
                    }));
                }
            } else {
                console.warn(`Image file not found: ${absoluteImgPath}`);
                children.push(new Paragraph({
                    children: [new TextRun({ text: `[Image Not Found: ${absoluteImgPath}]`, color: "FF0000" })]
                }));
            }
            inList = false;
            continue;
        }

        // --- Horizontal Rules ---
        if (line.match(/^(-{3,}|\*{3,}|_{3,})$/)) {
            children.push(new Paragraph({
                border: {
                    bottom: {
                        color: "auto",
                        space: 1,
                        style: "single",
                        size: 6,
                    },
                },
                spacing: { before: 120, after: 120 }
            }));
            inList = false;
            continue;
        }

        // --- Lists ---
        // Bullet: - or *
        const bulletMatch = line.match(/^(\s*)([-*])\s+(.*)/);
        // Number: 1.
        const numberMatch = line.match(/^(\s*)(\d+)\.\s+(.*)/);

        if (bulletMatch) {
            const indentLevel = bulletMatch[1].length / 2; // Assume 2 spaces per indent
            const text = bulletMatch[3];

            children.push(new Paragraph({
                numbering: {
                    reference: "bullet-list",
                    level: Math.floor(indentLevel)
                },
                children: parseInlineFormatting(text)
            }));
            continue;
        }

        if (numberMatch) {
            const indentLevel = numberMatch[1].length / 2;
            const text = numberMatch[3];

            children.push(new Paragraph({
                numbering: {
                    reference: "numbered-list",
                    level: Math.floor(indentLevel)
                },
                children: parseInlineFormatting(text)
            }));
            continue;
        }

        // --- Blockquotes ---
        if (line.startsWith('>')) {
            const text = line.replace(/^>\s*/, '').trim();
            children.push(new Paragraph({
                children: parseInlineFormatting(text),
                indent: { left: 720 }, // 0.5 inch indent
                border: {
                    left: {
                        color: "888888",
                        space: 120,
                        style: "single",
                        size: 24, // 3pt
                    }
                },
                style: "IntenseQuote" // Use a style if available, or just formatting
            }));
            inList = false;
            continue;
        }

        // --- Normal Paragraph ---
        // Treat as normal paragraph
        children.push(new Paragraph({
            children: parseInlineFormatting(line),
            spacing: { after: 120 } // Space after paragraphs
        }));
    }

    // Define Document
    const doc = new Document({
        numbering: {
            config: [
                {
                    reference: "bullet-list",
                    levels: [
                        { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
                        { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1440, hanging: 360 } } } }
                    ]
                },
                {
                    reference: "numbered-list",
                    levels: [
                        { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }
                    ]
                }
            ]
        },
        styles: {
            default: {
                document: {
                    run: {
                        font: "Arial",
                        size: 22, // 11pt
                    },
                },
            },
            paragraphStyles: [
                {
                    id: "IntenseQuote",
                    name: "Intense Quote",
                    basedOn: "Normal",
                    run: { italics: true, color: "555555" }
                }
            ]
        },
        sections: [{
            properties: {
                page: {
                    margin: {
                        top: convertInchesToTwip(1),
                        bottom: convertInchesToTwip(1),
                        left: convertInchesToTwip(1),
                        right: convertInchesToTwip(1),
                    },
                },
            },
            headers: {
                default: new Header({
                    children: [
                        new Paragraph({
                            children: [
                                new TextRun({ text: "The Animal Nutraceutical Landscape (2024-2030)", italics: true, size: 20 })
                            ],
                            alignment: AlignmentType.RIGHT
                        })
                    ]
                })
            },
            footers: {
                default: new Footer({
                    children: [
                        new Paragraph({
                            children: [
                                new TextRun({ children: [PageNumber.CURRENT] }),
                                new TextRun(" / "),
                                new TextRun({ children: [PageNumber.TOTAL_PAGES] })
                            ],
                            alignment: AlignmentType.CENTER
                        })
                    ]
                })
            },
            children: children
        }]
    });

    // Write File
    Packer.toBuffer(doc).then((buffer) => {
        fs.writeFileSync(OUTPUT_FILE, buffer);
        console.log(`Successfully generated DOCX at: ${OUTPUT_FILE}`);
    });
}

// Simple inline formatter for **bold** and *italic*
// This is non-recursive and limited for this specific task
function parseInlineFormatting(text) {
    const runs = [];
    let currentText = "";
    let isBold = false;
    let isItalic = false;

    // Simple parser? Or just regex split?
    // Regex split by bold markers
    // Example: "Text **Bold** Text" -> ["Text ", "**Bold**", " Text"]

    // A robust way without full parsing:
    // Split by ** or *
    // This is a naive implementation but sufficient for basic reports
    const parts = text.split(/(\*\*.*?\*\*|\*.*?\*)/g);

    parts.forEach(part => {
        if (part.startsWith('**') && part.endsWith('**')) {
            runs.push(new TextRun({
                text: part.slice(2, -2),
                bold: true
            }));
        } else if (part.startsWith('*') && part.endsWith('*')) {
            runs.push(new TextRun({
                text: part.slice(1, -1),
                italics: true
            }));
        } else if (part !== "") {
            runs.push(new TextRun({
                text: part
            }));
        }
    });

    // If naive split didn't find anything (empty runs), return the whole text
    if (runs.length === 0 && text.length > 0) {
        runs.push(new TextRun(text));
    }

    return runs;
}

generateDocx();
