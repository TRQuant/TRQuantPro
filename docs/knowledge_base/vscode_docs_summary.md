# VS Code Extension 开发文档摘要

生成时间: 2025-12-21 19:47:46

## 文档列表

### Webview API
- **URL**: https://code.visualstudio.com/api/extension-guides/webview
- **类别**: webview
- **标签**: webview, csp, message, typescript, extension
- **代码示例**: 20 个

**内容摘要**:
Webview API

The webview API allows extensions to create fully customizable views within Visual Studio Code. For example, the built-in Markdown extension uses webviews to render Markdown previews. Webviews can also be used to build complex user interfaces beyond what VS Code's native APIs support.

Think of a webview as an 
iframe
 within VS Code that your extension controls. A webview can render almost any HTML content in this frame, and it communicates with extensions using message passing. Th...

### VS Code API
- **URL**: https://code.visualstudio.com/api/references/vscode-api
- **类别**: extension_api
- **标签**: webview, react, mcp, csp, message, typescript, extension
- **代码示例**: 20 个

**内容摘要**:
VS Code API

VS Code API
 is a set of JavaScript APIs that you can invoke in your Visual Studio Code extension. This page lists all VS Code APIs available to extension authors.

API namespaces and classes

This listing is compiled from the 
vscode.d.ts
 file from the VS Code repository.

authentication

Namespace for authentication.

Events

onDidChangeSessions
: 
Event
<
AuthenticationSessionsChangeEvent
>

An 
Event
 which fires when the authentication sessions of an authentication provider ha...

### Extension Anatomy
- **URL**: https://code.visualstudio.com/api/get-started/extension-anatomy
- **类别**: extension_anatomy
- **标签**: typescript, extension
- **代码示例**: 3 个

**内容摘要**:
Extension Anatomy

In the last topic, you were able to get a basic extension running. How does it work under the hood?

The 
Hello World
 extension does 3 things:

Registers the 
onCommand
 
Activation Event
: 
onCommand:helloworld.helloWorld
, so the extension becomes activated when user runs the 
Hello World
 command.
Note:
 Starting with 
VS Code 1.74.0
, commands declared in the 
commands
 section of 
package.json
 automatically activate the extension when invoked, without requiring an expli...

### Activation Events
- **URL**: https://code.visualstudio.com/api/references/activation-events
- **类别**: activation_events
- **标签**: webview, typescript, extension
- **代码示例**: 20 个

**内容摘要**:
Activation Events

Activation Events
 is a set of JSON declarations that you make in the 
activationEvents
 field of 
package.json
 
Extension Manifest
. Your extension becomes activated when the 
Activation Event
 happens. Here is a list of all available 
Activation Events
:

onAuthenticationRequest

onChatParticipant

onCommand

onCustomEditor

onDebug

onDebugAdapterProtocolTracker

onDebugDynamicConfigurations

onDebugInitialConfigurations

onDebugResolve

onEditSession

onFileSystem

onIssu...
