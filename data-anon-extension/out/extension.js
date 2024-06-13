"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = __importStar(require("vscode"));
const python_shell_1 = require("python-shell");
const path_1 = __importDefault(require("path"));
// Default Working Azure Connection Details
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
function activate(context) {
    let disposable = vscode.commands.registerCommand('data-anon-extension.runAnonymisationDialog', () => {
        const panel = vscode.window.createWebviewPanel('anonymisationDialog', 'Data Anonymisation Dialog', vscode.ViewColumn.One, {
            enableScripts: true
        });
        panel.webview.html = getDatabaseSelectionWebviewContent();
        panel.webview.onDidReceiveMessage(message => {
            switch (message.command) {
                case 'open_db_cs':
                    console.log('open db cs:  ' + message.text);
                    connectAndQueryDB_plus_buildSelectionPage_cs(panel, message.text);
                    break;
                case 'open_db_config':
                    console.log('open db config:  ' + message.text);
                    connectAndQueryDB_plus_buildSelectionPage_config(panel, message.text);
                    break;
                case 'load_connection_form':
                    panel.webview.html = getDatabaseSelectionWebviewContent();
                    break;
                case 'report':
                    console.log("[Report]: " + message.text);
                    break;
            }
        }, undefined, context.subscriptions);
        //call_python();
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
function getDatabaseSelectionWebviewContent() {
    return `
		<!DOCTYPE html>
		<html lang="en">
			<head>
				<meta charset="UTF-8">
				<title>Test</title>
				<script>
					const vscode = acquireVsCodeApi();

					function message_connectionstring() {
						vscode.postMessage({
							command: 'open_db_cs',
							text: document.getElementById("connectionString").value
						});
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
					}
				</script>
			</head>
			<body>
				<h1>Select which Database to run Anonymization on</h1>

				<hr>

				Connection String<br>
				<input type="text" id="connectionString"/> <button onclick="message_connectionstring()">Open</button>

				<hr>
				SQL-Connection<br>
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
function connectAndQueryDB_plus_buildSelectionPage_cs(panel, given_cs) {
    connectAndQueryDB_plus_buildSelectionPage(panel, given_cs);
}
function connectAndQueryDB_plus_buildSelectionPage_config(panel, given_config) {
    let split = given_config.split(";", 4);
    let config = {
        user: split[0],
        password: split[1],
        server: split[2],
        database: split[3],
    };
    connectAndQueryDB_plus_buildSelectionPage(panel, config);
}
function connectAndQueryDB_plus_buildSelectionPage(panel, connection_object) {
    let sql = require("mssql");
    // Establish connection using either config or connectionstring
    sql.connect(connection_object, function (err) {
        if (err) {
            panel.webview.html += "err: " + err + "<br>";
        }
        let request = new sql.Request();
        request.query('SELECT * FROM INFORMATION_SCHEMA.TABLES', function (err, recordset) {
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
            for (let i = 0; i < recordset_length; i++) {
                constructed_page += "<li>";
                constructed_page += '<input type="checkbox"> ';
                constructed_page += recordset_by_itself[i].TABLE_NAME;
                constructed_page += "</li>";
            }
            // SETUP End of Page
            constructed_page += `
					</ul>
					<button>Run</button>
					<button onclick="message_go_back()">Go Back</button>
				</body>
			</html>
			`;
            panel.webview.html = constructed_page;
        });
    });
}
function call_python() {
    python_shell_1.PythonShell.run(path_1.default.join(__dirname, '..', '..', 'src', 'app.py'), undefined).then(messages => {
        console.log('finished');
    });
}
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map