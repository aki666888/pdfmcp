#!/usr/bin/env node
/**
 * MCP Bridge Server - Node.js version
 * Connects Claude Desktop to your Python PDF filler
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { spawn } from 'child_process';
import { writeFileSync, unlinkSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Create MCP server
const server = new Server(
  {
    name: 'pharmacare-bridge',
    version: '1.0.0',
  },
  {
    capabilities: {},
  }
);

// Define the fill_form tool
server.setRequestHandler('tools/list', async () => ({
  tools: [
    {
      name: 'fill_form',
      description: 'Fill PharmaCare form with provided data',
      inputSchema: {
        type: 'object',
        properties: {
          patient_name: {
            type: 'string',
            description: 'Patient full name'
          },
          phn: {
            type: 'string',
            description: '10-digit PHN'
          },
          phone: {
            type: 'string',
            description: 'Phone number'
          },
          condition_numbers: {
            type: 'array',
            items: { type: 'number' },
            description: 'Array of condition box numbers'
          },
          symptoms: {
            type: 'string',
            description: 'Patient symptoms'
          },
          medical_history: {
            type: 'string',
            description: 'Medical history'
          },
          diagnosis: {
            type: 'string',
            description: 'Diagnosis'
          },
          medication: {
            type: 'string',
            description: 'Medication details'
          }
        },
        required: ['patient_name', 'phn']
      }
    }
  ]
}));

// Handle tool calls
server.setRequestHandler('tools/call', async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === 'fill_form') {
    try {
      console.error('Received form data:', JSON.stringify(args, null, 2));
      
      // Create a temporary JSON file with the data
      const tempFile = join(__dirname, 'temp_form_data.json');
      writeFileSync(tempFile, JSON.stringify(args));
      
      // Call the Python script
      return new Promise((resolve, reject) => {
        const pythonPath = 'C:\\Program Files\\Python312\\python.exe';
        const scriptPath = join(__dirname, 'bridge_runner.py');
        
        const python = spawn(pythonPath, [scriptPath, tempFile]);
        
        let output = '';
        let error = '';
        
        python.stdout.on('data', (data) => {
          output += data.toString();
        });
        
        python.stderr.on('data', (data) => {
          error += data.toString();
          console.error('Python stderr:', data.toString());
        });
        
        python.on('close', (code) => {
          // Clean up temp file
          try {
            unlinkSync(tempFile);
          } catch (e) {
            // Ignore cleanup errors
          }
          
          if (code !== 0) {
            resolve({
              content: [{
                type: 'text',
                text: `Error: Process exited with code ${code}\n${error}`
              }]
            });
          } else {
            resolve({
              content: [{
                type: 'text',
                text: output || 'Form processed successfully'
              }]
            });
          }
        });
        
        python.on('error', (err) => {
          resolve({
            content: [{
              type: 'text',
              text: `Error spawning Python: ${err.message}`
            }]
          });
        });
      });
      
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: `Error: ${error.message}`
        }]
      };
    }
  }
  
  return {
    content: [{
      type: 'text',
      text: `Unknown tool: ${name}`
    }]
  };
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('PharmaCare Bridge Server (Node.js) started');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});