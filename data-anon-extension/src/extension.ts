/* Imports */
import * as vscode from 'vscode';
import mssql = require('mssql');
import {PythonShell} from 'python-shell';
import path from 'path';

/* Global Variables */
var used_config : any | undefined;
var used_cs: string | undefined;

/* Connection Details for Azure DB; for copy & pasting or testing */
let default_config = {
	user: 'data-anon',
	password: 'Lantanio13891!',
	server: 'sqls-dataanon-dev-001.database.windows.net', 
	database: 'Northwind',
	options: {
		encrypt: true
	}
};
let default_cs = 'Server=tcp:sqls-dataanon-dev-001.database.windows.net,1433;Initial Catalog=Northwind;Persist Security Info=False;User ID=data-anon;Password=Lantanio13891!;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;';

/* Action performed when Command is activated */
export function activate(context: vscode.ExtensionContext) {
	let disposable = vscode.commands.registerCommand('data-anon-extension.runAnonymisationDialog', () => {
		const panel = vscode.window.createWebviewPanel(
			'anonymisationDialog',
			'Data Anonymisation Dialog',
			vscode.ViewColumn.One,
			{
				enableScripts: true
			}
		);

		panel.webview.html = getDatabaseSelectionWebviewContent();

		panel.webview.onDidReceiveMessage(
			message => {
				switch (message.command) {
					case 'open_db_cs':
						console.log('open db cs:  ' + message.text);

						used_cs = message.text;
						
						connectAndQueryDB_plus_buildSelectionPage(panel);
						break;
					case 'open_db_config':
						console.log('open db config:  ' + message.text);

						used_config = config_string_to_config(message.text);
						
						connectAndQueryDB_plus_buildSelectionPage(panel);
						break;

					case 'load_connection_form':
						panel.webview.html = getDatabaseSelectionWebviewContent();
						break;

					case 'python':
						write_order(message.text);
						//call_python();
						panel.webview.html = getDatabaseSelectionWebviewContent();
						break;

					case 'report':
						console.log("[Report]: " + message.text);
						break;
				}
			},
			undefined,
        	context.subscriptions
		);
	});

	context.subscriptions.push(disposable);
}

/* Builds HTML for Database Connecting */
function getDatabaseSelectionWebviewContent() {
	used_cs = undefined;
	used_config = undefined;
	return `
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="UTF-8">
				<title>Test</title>
				<script>
					const vscode = acquireVsCodeApi();

					function message_default_cs() {
						vscode.postMessage({
							command: 'open_db_cs',
							text: 'Server=tcp:sqls-dataanon-dev-001.database.windows.net,1433;Initial Catalog=Northwind;Persist Security Info=False;User ID=data-anon;Password=Lantanio13891!;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;'
						});
						show_trying_to_open();
					}

					function message_default_config() {
						vscode.postMessage({
							command: 'open_db_config',
							text: 'data-anon;Lantanio13891!;sqls-dataanon-dev-001.database.windows.net;Northwind'
						});
						show_trying_to_open();
					}

					function message_connectionstring() {
						
						vscode.postMessage({
							command: 'open_db_cs',
							text: document.getElementById("connectionString").value
						});
						show_trying_to_open();
					}
					function message_config() {
						let user = document.getElementById("user").value;
						let password = document.getElementById("password").value;
						let server = document.getElementById("server").value;
						let database = document.getElementById("database").value;
						
						vscode.postMessage({
							command: 'open_db_config',
							text: user + ";" + password + ";" + server + ";" + database
						});
						show_trying_to_open();
					}
					function show_trying_to_open() {
						document.body.innerHTML = "Loading ...";
					}
				</script>
			</head>
			<body>
				<h1>Select which Database to run Anonymization on</h1>

				<hr>

				<p onclick="message_default_cs()">Connection String</p>
				<input type="text" id="connectionString"/> <button onclick="message_connectionstring()">Open</button>

				<hr>
				<p onclick="message_default_config()">SQL-Connection</p>
				User <input id="user"/><br>
				Password <input id="password"/><br>
				Server <input id="server"/><br>
				Database <input id="database"/><br>
				<button onclick="message_config()">Open</button>
				

				<hr>

				<p>
					You will be given the choice over which tables to anonymize later.
				</p>
			</body>
		</html>
	`;
}

/* Turns a string into a config */
function config_string_to_config(given_config: string) {
	let split = given_config.split(";", 4);
	let config = {
		user: split[0],
		password: split[1],
		server: split[2],
		database: split[3],
	};
	return config;
}

/* Builds Table-Selection HTML by connecting to server using global vars */
function connectAndQueryDB_plus_buildSelectionPage(panel: any) {
	let sql = require("mssql");

	// Establish connection using either config or connectionstring
	let connection_object;
	if(used_cs !== undefined) {
		connection_object = used_cs;
	}
	else if(used_config !== undefined) {
		connection_object = used_config;
	}
	else {
		connection_object = undefined;
	}
	sql.connect(connection_object, function (err: any) {
		if (err) {
			panel.webview.html += "err: " + err + "<br>";
		}
		
		let request = new sql.Request();

		request.query('SELECT * FROM INFORMATION_SCHEMA.TABLES', function (err: any, recordset: any) {
		
			if (err) {
				panel.webview.html += "err: " + err + "<br>";
			}

			// SETUP Beginning of Page
			let constructed_page = `
			<!DOCTYPE html>
			<html lang="en">
				<head>
					<meta charset="UTF-8">
					<title>Test</title>
					<style>
						ul {
							margin: 0;
							list-style: none;
						}
					</style>
					<script>
						function message_go_back() {
							const vscode = acquireVsCodeApi();

							vscode.postMessage({
								command: 'load_connection_form',
								text: ''
							});
						}

						function hand_over_to_python() {
							const vscode = acquireVsCodeApi();

							let tables = "";
							let items = document.getElementsByTagName("li");
							for(let i=0; i < items.length; i++) {
								let item = items[i];
								if(item.getElementsByTagName("input")[0].checked)
									tables += item.getElementsByTagName("span")[0].innerHTML + "\\n";
							}

							vscode.postMessage({
								command: 'python',
								text: tables
							});
						}
					</script>
				</head>
				<body>
					<h1>Select which Tables to run Anonymization on</h1>
	
					<hr>
	
					<ul>
			`;

			// ADD Tables to Selection page
			let recordset_by_itself = recordset.recordset;
			let recordset_length = recordset_by_itself.length;
			for(let i = 0; i < recordset_length; i++) {
				constructed_page += "<li>";
				constructed_page += '<input type="checkbox"> ';
				constructed_page += '<span>' + recordset_by_itself[i].TABLE_NAME + '</span>';
				constructed_page += "</li>";
			}

			// SETUP End of Page
			constructed_page += `
					</ul>
					<button onclick="hand_over_to_python()">Run</button>
					<button onclick="message_go_back()">Go Back</button>
				</body>
			</html>
			`;

			panel.webview.html = constructed_page;
		});
	});
}

/* Function calling Python */
function call_python() {
	PythonShell.run(path.join(__dirname, '..', '..', 'src', 'app.py'), undefined).then(messages=>{
		console.log('finished');
	});
}

/* 	Function that writes details for an anonymization order to a file for python.
	Draws Connection details from global vars.
*/
function write_order(tables: string) {
	const fs = require('fs');

	let path_string = path.join(__dirname, '..', '..', 'order');

	// Build content of order
	let content = "[Anonymization Order]\n";
	
	let connection_section;
	if(used_cs !== undefined) {
		connection_section = "[Connection String]\n";
		connection_section += used_cs + "\n";
	}
	else if(used_config !== undefined) {
		connection_section = "[Config]\n";
		connection_section += used_config.user + "\n";
		connection_section += used_config.password + "\n";
		connection_section += used_config.server + "\n";
		connection_section += used_config.database + "\n";
	}
	else {
		connection_section = "erroneus state";
	}
	content += connection_section;

	content += "[TABLES]\n";
	content += tables;

	// Write order to file
	fs.writeFile(path_string, content, function(err : any) {
		if(err) {
			return console.log(err);
		}
		console.log("The file was saved!");
	}); 
}

export function deactivate() {}
