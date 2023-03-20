odoo.define('web.web_widget_flow_chart', function (require) {
    "use strict";
var field_registry = require('web.field_registry');
    var fields = require('web.basic_fields');
   
    var formats=require('web.field_utils');

    var FieldFlowChart = fields.FieldChar.extend({
        template: "FieldFlowChart",
        
        widget_class: 'o_form_field_flow_chart',
        events: {
            'change input': 'store_dom_value',
            'click #print':'printDiagram'
            

        },
         
        start:function(){
          console.log(this);
          this.initialized=false;            
          this.myDiagram=null;
          this.default={ "class": "go.GraphLinksModel",
            "linkFromPortIdProperty": "fromPort",
            "linkToPortIdProperty": "toPort",
            "nodeDataArray": [
          ],
            "linkDataArray": [
          ]};
              this.$$ = go.GraphObject.make;  // for conciseness in defining templates

          this.idag=null;
          this._super.apply(this, arguments);

      },
        handleCommand:function(e){
          var self=this;
          var id=$(e.target).attr('id');
          if(id=='Delete'){
            self.myDiagram.commandHandler.deleteSelection()
          }
          if(id=='Cut'){
            self.myDiagram.commandHandler.cutSelection()
          }
          if(id=='Copy'){
            self.myDiagram.commandHandler.copySelection()
          }
          if(id=='Paste'){
            self.myDiagram.commandHandler.pasteSelection()
          }
        },
       
      simple_go:function(){

          var self=this;
          self.diag = self.$$(go.Diagram,"diagram_display");

      // when the document is modified, add a "*" to the title and enable the "Save" button
     

      // helper definitions for node templates

      function nodeStyle() {
        return [
        new go.Binding("angle").makeTwoWay(),
        new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify),
          // The Node.location comes from the "loc" property of the node data,
          // converted by the Point.parse static method.
          // If the Node.location is changed, it updates the "loc" property of the node data,
          // converting back using the Point.stringify static method.
          new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
          {
            // the Node.location is at the center of each node
            locationSpot: go.Spot.Center,
            resizable:true,
            rotatable:true,
            resizeObjectName:'ITEM',
            selectionObjectName:'ITEM'
            
          }
        ];
      }

      // Define a function for creating a "port" that is normally transparent.
      // The "name" is used as the GraphObject.portId,
      // the "align" is used to determine where to position the port relative to the body of the node,
      // the "spot" is used to control how links connect with the port and whether the port
      // stretches along the side of the node,
      // and the boolean "output" and "input" arguments control whether the user can draw links from or to the port.
      function makePort(name, align, spot, output, input) {
        var horizontal = align.equals(go.Spot.Top) || align.equals(go.Spot.Bottom);
        // the port is basically just a transparent rectangle that stretches along the side of the node,
        // and becomes colored when the mouse passes over it
        return self.$$(go.Shape,
          {
            fill: "transparent",  // changed to a color in the mouseEnter event handler
            strokeWidth: 0,  // no stroke
            width: horizontal ? NaN : 8,  // if not stretching horizontally, just 8 wide
            height: !horizontal ? NaN : 8,  // if not stretching vertically, just 8 tall
            alignment: align,  // align the port on the main Shape
            stretch: (horizontal ? go.GraphObject.Horizontal : go.GraphObject.Vertical),
            portId: name,  // declare this object to be a "port"
            fromSpot: spot,  // declare where links may connect at this port
            fromLinkable: output,  // declare whether the user may draw links from here
            toSpot: spot,  // declare where links may connect at this port
            toLinkable: input,  // declare whether the user may draw links to here
            cursor: "pointer",  // show a different cursor to indicate potential link point
            mouseEnter: function(e, port) {  // the PORT argument will be this Shape
              if (!e.diagram.isReadOnly) port.fill = "rgba(255,0,255,0.5)";
            },
            mouseLeave: function(e, port) {
              port.fill = "transparent";
            }
          });
      }

      function textStyle() {
        return {
          font: "bold 18pt Lato, Helvetica, Arial, sans-serif",
          stroke: "#000000"
        }
      }

      // define the Node templates for regular nodes

      self.diag.nodeTemplateMap.add("",  // the default category
        self.$$(go.Node, "Table", nodeStyle(),
          // the main object is a Panel that surrounds a TextBlock with a rectangular Shape
          self.$$(go.Panel, "Auto",
            self.$$(go.Shape, "Rectangle",
              { name:'ITEM',fill: "#ffffff", stroke: "#000000", strokeWidth: 3.5 },
              new go.Binding("figure", "figure"),
                      new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify)
),
            self.$$(go.TextBlock, textStyle(),
              {
                margin: 8,
                maxSize: new go.Size(400, NaN),
                wrap: go.TextBlock.WrapFit,
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          ),
          // four named ports, one on each side:
          makePort("T", go.Spot.Top, go.Spot.TopSide, false, true),
          makePort("L", go.Spot.Left, go.Spot.LeftSide, true, true),
          makePort("R", go.Spot.Right, go.Spot.RightSide, true, true),
          makePort("B", go.Spot.Bottom, go.Spot.BottomSide, true, false)
        ));

      self.diag.nodeTemplateMap.add("Conditional",
        self.$$(go.Node, "Table", nodeStyle(),
          // the main object is a Panel that surrounds a TextBlock with a rectangular Shape
          self.$$(go.Panel, "Auto",
            self.$$(go.Shape, "Diamond",
              { name:'ITEM',fill: "#ffffff", stroke: "blue", strokeWidth: 3.5 },
              new go.Binding("figure", "figure"),
                      new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify),
),
            self.$$(go.TextBlock, textStyle(),
              {
                margin: 8,
                maxSize: new go.Size(160, NaN),
                wrap: go.TextBlock.WrapFit,
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          ),
          // four named ports, one on each side:
          makePort("T", go.Spot.Top, go.Spot.Top, false, true),
          makePort("L", go.Spot.Left, go.Spot.Left, true, true),
          makePort("R", go.Spot.Right, go.Spot.Right, true, true),
          makePort("B", go.Spot.Bottom, go.Spot.Bottom, true, false)
        ));

      self.diag.nodeTemplateMap.add("Start",
        self.$$(go.Node, "Table", nodeStyle(),
          self.$$(go.Panel, "Spot",
            self.$$(go.Shape, "Circle",
              {name:'ITEM', fill: "#ffffff", stroke: "green", strokeWidth: 3.5 },        new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify),
),

           self.$$(go.TextBlock, textStyle(),
              {
                margin: 8,
                maxSize: new go.Size(160, NaN),
                wrap: go.TextBlock.WrapFit,
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          ),
          // three named ports, one on each side except the top, all output only:
          makePort("L", go.Spot.Left, go.Spot.Left, true, false),
          makePort("R", go.Spot.Right, go.Spot.Right, true, false),
          makePort("B", go.Spot.Bottom, go.Spot.Bottom, true, false)
        ));

      self.diag.nodeTemplateMap.add("End",
        self.$$(go.Node, "Table", nodeStyle(),
          self.$$(go.Panel, "Spot",
            self.$$(go.Shape, "Circle",
              { name:'ITEM', fill: "#ffffff", stroke: "red", strokeWidth: 3.5 },        new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify),
),
            self.$$(go.TextBlock, textStyle(),
              {
                margin: 8,
                maxSize: new go.Size(160, NaN),
                wrap: go.TextBlock.WrapFit,
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          ),
          // three named ports, one on each side except the bottom, all input only:
          makePort("T", go.Spot.Top, go.Spot.Top, false, true),
          makePort("L", go.Spot.Left, go.Spot.Left, false, true),
          makePort("R", go.Spot.Right, go.Spot.Right, false, true)
        ));

      // taken from ../extensions/Figures.js:
      go.Shape.defineFigureGenerator("File", function(shape, w, h) {
        var geo = new go.Geometry();
        var fig = new go.PathFigure(0, 0, true); // starting point
        geo.add(fig);
        fig.add(new go.PathSegment(go.PathSegment.Line, .75 * w, 0));
        fig.add(new go.PathSegment(go.PathSegment.Line, w, .25 * h));
        fig.add(new go.PathSegment(go.PathSegment.Line, w, h));
        fig.add(new go.PathSegment(go.PathSegment.Line, 0, h).close());
        var fig2 = new go.PathFigure(.75 * w, 0, false);
        geo.add(fig2);
        // The Fold
        fig2.add(new go.PathSegment(go.PathSegment.Line, .75 * w, .25 * h));
        fig2.add(new go.PathSegment(go.PathSegment.Line, w, .25 * h));
        geo.spot1 = new go.Spot(0, .25);
        geo.spot2 = go.Spot.BottomRight;
        return geo;
      });

      self.diag.nodeTemplateMap.add("Comment",
        self.$$(go.Node, "Auto", nodeStyle(),
          self.$$(go.Shape, "File",
            { name:'ITEM',fill: "yellow", stroke: "#000000", strokeWidth: 3 }),
          self.$$(go.TextBlock, textStyle(),
            {
              margin: 8,
              maxSize: new go.Size(200, NaN),
              wrap: go.TextBlock.WrapFit,
              textAlign: "center",
              editable: true
            },
            new go.Binding("text").makeTwoWay())
          // no ports, because no links are allowed to connect with a comment
        ));


      // replace the default Link template in the linkTemplateMap
      self.diag.linkTemplate =
        self.$$(go.Link,  // the whole link panel
          {
            routing: go.Link.AvoidsNodes,
            curve: go.Link.JumpOver,
            corner: 5, toShortLength: 4,
            relinkableFrom: true,
            relinkableTo: true,
            reshapable: true,
            resegmentable: true,
            // mouse-overs subtly highlight links:
            mouseEnter: function(e, link) { link.findObject("HIGHLIGHT").stroke = "rgba(30,144,255,0.2)"; },
            mouseLeave: function(e, link) { link.findObject("HIGHLIGHT").stroke = "transparent"; },
            selectionAdorned: false
          },
          new go.Binding("points").makeTwoWay(),
          self.$$(go.Shape,  // the highlight shape, normally transparent
            { isPanelMain: true, strokeWidth: 8, stroke: "transparent", name: "HIGHLIGHT" }),
          self.$$(go.Shape,  // the link path shape
            { isPanelMain: true, stroke: "gray", strokeWidth: 2 },
            new go.Binding("stroke", "isSelected", function(sel) { return sel ? "dodgerblue" : "gray"; }).ofObject()),
          self.$$(go.Shape,  // the arrowhead
            { toArrow: "standard", strokeWidth: 0, fill: "gray" }),
          self.$$(go.Panel, "Auto",  // the link label, normally not visible
            { visible: false, name: "LABEL", segmentIndex: 2, segmentFraction: 0.5 },
            new go.Binding("visible", "visible").makeTwoWay(),
            self.$$(go.Shape, "RoundedRectangle",  // the label shape
              { fill: "#F8F8F8", strokeWidth: 0 }),
            self.$$(go.TextBlock, "Yes",  // the label
              {
                textAlign: "center",
                font: "10pt helvetica, arial, sans-serif",
                stroke: "#333333",
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          )
        );

      // Make link labels visible if coming out of a "conditional" node.
      // This listener is called by the "LinkDrawn" and "LinkRelinked" DiagramEvents.
      function showLinkLabel(e) {
        var label = e.subject.findObject("LABEL");
        if (label !== null) label.visible = (e.subject.fromNode.data.category === "Conditional");
      }
      },
      printDiagram:function() {
        var self=this;
      var svgWindow = window.open();
      if (!svgWindow) return;  // failure to open a new Window
      var printSize = new go.Size(700, 960);
      var bnds = self.diag.documentBounds;
      var x = bnds.x;
      var y = bnds.y;
      while (y < bnds.bottom) {
        while (x < bnds.right) {
          var svg = self.diag.makeSVG({ scale: 1.0, position: new go.Point(x, y), size: printSize });
          svgWindow.document.body.appendChild(svg);
          x += printSize.width;
        }
        x = bnds.x;
        y += printSize.height;
      }
      setTimeout(function() { svgWindow.print(); }, 1);
    },
        init_go:function(){

        	var self=this;
      self.myDiagram =
        self.$$(go.Diagram, "diagram_edit",  // must name or refer to the DIV HTML element
          {
            "LinkDrawn": showLinkLabel,  // this DiagramEvent listener is defined below
            "LinkRelinked": showLinkLabel,
            "undoManager.isEnabled": true,
            "contextMenuTool.isEnabled":true,
            "zoomToFit":true,
            "grid.visible":true,
            "grid.gridCellSize":new go.Size(100,100),
            "draggingTool.isGridSnapEnabled":true,
            "draggingTool.gridSnapCellSize":new go.Size(50,50),
              // enable undo & redo
          });

      // when the document is modified, add a "*" to the title and enable the "Save" button
      self.myDiagram.addDiagramListener("Modified", function(e) {
        var button = document.getElementById("SaveButton");
        if (button) button.disabled = !self.myDiagram.isModified;
        var idx = document.title.indexOf("*");
        if (self.myDiagram.isModified) {
          if (idx < 0) document.title += "*";
        } else {
          if (idx >= 0) document.title = document.title.substr(0, idx);
        }
      });

      // helper definitions for node templates

      function nodeStyle() {
        return [
        new go.Binding("angle").makeTwoWay(),
        new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify),
          // The Node.location comes from the "loc" property of the node data,
          // converted by the Point.parse static method.
          // If the Node.location is changed, it updates the "loc" property of the node data,
          // converting back using the Point.stringify static method.
          new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
          {
            // the Node.location is at the center of each node
            locationSpot: go.Spot.Center,
            resizable:true,
            rotatable:true,
            resizeObjectName:'ITEM',
            selectionObjectName:'ITEM'
            
          }
        ];
      }

      // Define a function for creating a "port" that is normally transparent.
      // The "name" is used as the GraphObject.portId,
      // the "align" is used to determine where to position the port relative to the body of the node,
      // the "spot" is used to control how links connect with the port and whether the port
      // stretches along the side of the node,
      // and the boolean "output" and "input" arguments control whether the user can draw links from or to the port.
      function makePort(name, align, spot, output, input) {
        var horizontal = align.equals(go.Spot.Top) || align.equals(go.Spot.Bottom);
        // the port is basically just a transparent rectangle that stretches along the side of the node,
        // and becomes colored when the mouse passes over it
        return self.$$(go.Shape,
          {
            fill: "transparent",  // changed to a color in the mouseEnter event handler
            strokeWidth: 0,  // no stroke
            width: horizontal ? NaN : 8,  // if not stretching horizontally, just 8 wide
            height: !horizontal ? NaN : 8,  // if not stretching vertically, just 8 tall
            alignment: align,  // align the port on the main Shape
            stretch: (horizontal ? go.GraphObject.Horizontal : go.GraphObject.Vertical),
            portId: name,  // declare this object to be a "port"
            fromSpot: spot,  // declare where links may connect at this port
            fromLinkable: output,  // declare whether the user may draw links from here
            toSpot: spot,  // declare where links may connect at this port
            toLinkable: input,  // declare whether the user may draw links to here
            cursor: "pointer",  // show a different cursor to indicate potential link point
            mouseEnter: function(e, port) {  // the PORT argument will be this Shape
              if (!e.diagram.isReadOnly) port.fill = "rgba(255,0,255,0.5)";
            },
            mouseLeave: function(e, port) {
              port.fill = "transparent";
            }
          });
      }

      function textStyle() {
        return {
          font: "bold 18pt Lato, Helvetica, Arial, sans-serif",
          stroke: "#000000"
        }
      }

      // define the Node templates for regular nodes

      self.myDiagram.nodeTemplateMap.add("",  // the default category
        self.$$(go.Node, "Table", nodeStyle(),
          // the main object is a Panel that surrounds a TextBlock with a rectangular Shape
          self.$$(go.Panel, "Auto",
            self.$$(go.Shape, "Rectangle",
              { name:'ITEM',fill: "#ffffff", stroke: "#000000", strokeWidth: 3.5 },
              new go.Binding("figure", "figure"),
                      new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify)
),
            self.$$(go.TextBlock, textStyle(),
              {
                margin: 8,
                maxSize: new go.Size(400, NaN),
                wrap: go.TextBlock.WrapFit,
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          ),
          // four named ports, one on each side:
          makePort("T", go.Spot.Top, go.Spot.TopSide, false, true),
          makePort("L", go.Spot.Left, go.Spot.LeftSide, true, true),
          makePort("R", go.Spot.Right, go.Spot.RightSide, true, true),
          makePort("B", go.Spot.Bottom, go.Spot.BottomSide, true, false)
        ));

      self.myDiagram.nodeTemplateMap.add("Conditional",
        self.$$(go.Node, "Table", nodeStyle(),
          // the main object is a Panel that surrounds a TextBlock with a rectangular Shape
          self.$$(go.Panel, "Auto",
            self.$$(go.Shape, "Diamond",
              { name:'ITEM',fill: "#ffffff", stroke: "blue", strokeWidth: 3.5 },
              new go.Binding("figure", "figure"),
                      new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify),
),
            self.$$(go.TextBlock, textStyle(),
              {
                margin: 8,
                maxSize: new go.Size(160, NaN),
                wrap: go.TextBlock.WrapFit,
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          ),
          // four named ports, one on each side:
          makePort("T", go.Spot.Top, go.Spot.Top, false, true),
          makePort("L", go.Spot.Left, go.Spot.Left, true, true),
          makePort("R", go.Spot.Right, go.Spot.Right, true, true),
          makePort("B", go.Spot.Bottom, go.Spot.Bottom, true, false)
        ));

      self.myDiagram.nodeTemplateMap.add("Start",
        self.$$(go.Node, "Table", nodeStyle(),
          self.$$(go.Panel, "Spot",
            self.$$(go.Shape, "Circle",
              {name:'ITEM', fill: "#ffffff", stroke: "green", strokeWidth: 3.5 },        new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify),
),

           self.$$(go.TextBlock, textStyle(),
              {
                margin: 8,
                maxSize: new go.Size(160, NaN),
                wrap: go.TextBlock.WrapFit,
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          ),
          // three named ports, one on each side except the top, all output only:
          makePort("L", go.Spot.Left, go.Spot.Left, true, false),
          makePort("R", go.Spot.Right, go.Spot.Right, true, false),
          makePort("B", go.Spot.Bottom, go.Spot.Bottom, true, false)
        ));

      self.myDiagram.nodeTemplateMap.add("End",
        self.$$(go.Node, "Table", nodeStyle(),
          self.$$(go.Panel, "Spot",
            self.$$(go.Shape, "Circle",
              { name:'ITEM', fill: "#ffffff", stroke: "red", strokeWidth: 3.5 },        new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify),
),
            self.$$(go.TextBlock, textStyle(),
              {
                margin: 8,
                maxSize: new go.Size(160, NaN),
                wrap: go.TextBlock.WrapFit,
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          ),
          // three named ports, one on each side except the bottom, all input only:
          makePort("T", go.Spot.Top, go.Spot.Top, false, true),
          makePort("L", go.Spot.Left, go.Spot.Left, false, true),
          makePort("R", go.Spot.Right, go.Spot.Right, false, true)
        ));

      // taken from ../extensions/Figures.js:
      go.Shape.defineFigureGenerator("File", function(shape, w, h) {
        var geo = new go.Geometry();
        var fig = new go.PathFigure(0, 0, true); // starting point
        geo.add(fig);
        fig.add(new go.PathSegment(go.PathSegment.Line, .75 * w, 0));
        fig.add(new go.PathSegment(go.PathSegment.Line, w, .25 * h));
        fig.add(new go.PathSegment(go.PathSegment.Line, w, h));
        fig.add(new go.PathSegment(go.PathSegment.Line, 0, h).close());
        var fig2 = new go.PathFigure(.75 * w, 0, false);
        geo.add(fig2);
        // The Fold
        fig2.add(new go.PathSegment(go.PathSegment.Line, .75 * w, .25 * h));
        fig2.add(new go.PathSegment(go.PathSegment.Line, w, .25 * h));
        geo.spot1 = new go.Spot(0, .25);
        geo.spot2 = go.Spot.BottomRight;
        return geo;
      });

      self.myDiagram.nodeTemplateMap.add("Comment",
        self.$$(go.Node, "Auto", nodeStyle(),
          self.$$(go.Shape, "File",
            { name:'ITEM',fill: "yellow", stroke: "#000000", strokeWidth: 3 },new go.Binding("desiredSize","size",go.Size.parse).makeTwoWay(go.Size.stringify)),
          self.$$(go.TextBlock, textStyle(),
            {
              margin: 8,
              maxSize: new go.Size(200, NaN),
              wrap: go.TextBlock.WrapFit,
              textAlign: "center",
              editable: true
            },
            new go.Binding("text").makeTwoWay())
          // no ports, because no links are allowed to connect with a comment
        ));


      // replace the default Link template in the linkTemplateMap
      self.myDiagram.linkTemplate =
        self.$$(go.Link,  // the whole link panel
          {
            routing: go.Link.AvoidsNodes,
            curve: go.Link.JumpOver,
            corner: 5, toShortLength: 4,
            relinkableFrom: true,
            relinkableTo: true,
            reshapable: true,
            resegmentable: true,
            // mouse-overs subtly highlight links:
            mouseEnter: function(e, link) { link.findObject("HIGHLIGHT").stroke = "rgba(30,144,255,0.2)"; },
            mouseLeave: function(e, link) { link.findObject("HIGHLIGHT").stroke = "transparent"; },
            selectionAdorned: false
          },
          new go.Binding("points").makeTwoWay(),
          self.$$(go.Shape,  // the highlight shape, normally transparent
            { isPanelMain: true, strokeWidth: 8, stroke: "transparent", name: "HIGHLIGHT" }),
          self.$$(go.Shape,  // the link path shape
            { isPanelMain: true, stroke: "gray", strokeWidth: 2 },
            new go.Binding("stroke", "isSelected", function(sel) { return sel ? "dodgerblue" : "gray"; }).ofObject()),
          self.$$(go.Shape,  // the arrowhead
            { toArrow: "standard", strokeWidth: 0, fill: "gray" }),
          self.$$(go.Panel, "Auto",  // the link label, normally not visible
            { visible: false, name: "LABEL", segmentIndex: 2, segmentFraction: 0.5 },
            new go.Binding("visible", "visible").makeTwoWay(),
            self.$$(go.Shape, "RoundedRectangle",  // the label shape
              { fill: "#F8F8F8", strokeWidth: 0 }),
            self.$$(go.TextBlock, "Yes",  // the label
              {
                textAlign: "center",
                font: "10pt helvetica, arial, sans-serif",
                stroke: "#333333",
                editable: true
              },
              new go.Binding("text").makeTwoWay())
          )
        );

      // Make link labels visible if coming out of a "conditional" node.
      // This listener is called by the "LinkDrawn" and "LinkRelinked" DiagramEvents.
      function showLinkLabel(e) {
        var label = e.subject.findObject("LABEL");
        if (label !== null) label.visible = (e.subject.fromNode.data.category === "Conditional");
      }

      // temporary links used by LinkingTool and RelinkingTool are also orthogonal:
      self.myDiagram.toolManager.linkingTool.temporaryLink.routing = go.Link.Orthogonal;
      self.myDiagram.toolManager.relinkingTool.temporaryLink.routing = go.Link.Orthogonal;

      self.load();  // load an initial diagram from some JSON text
function enable(name, ok) {
    var button = document.getElementById(name);
    if (button) button.disabled = !ok;
  }
  // enable or disable all command buttons
  function enableAll() {
    var cmdhnd = self.myDiagram.commandHandler;
    enable("Cut", cmdhnd.canCutSelection());
    enable("Copy", cmdhnd.canCopySelection());
    enable("Paste", cmdhnd.canPasteSelection());
    enable("Delete", cmdhnd.canDeleteSelection());
 
  }
  // notice whenever the selection may have changed
  self.myDiagram.addDiagramListener("ChangedSelection", function(e) {
    enableAll();
  });
  // notice when the Paste command may need to be reenabled
  self.myDiagram.addDiagramListener("ClipboardChanged", function(e) {
    enableAll();
  });
  // notice whenever a transaction or undo/redo has occurred
  self.myDiagram.addModelChangedListener(function(e) {
    if (e.isTransactionFinished) enableAll();
    self._setValue(self.myDiagram.model.toJson());
   // self.commitChanges(self.myDiagram.model.toJson());

  });
  // perform initial enablements after everything has settled down
  setTimeout(enableAll, 1000);

      // initialize the Palette that is on the left side of the page
      self.myPalette =
        self.$$(go.Palette, "palette",  // must name or refer to the DIV HTML element
          {
            // Instead of the default animation, use a custom fade-down
            "animationManager.initialAnimationStyle": go.AnimationManager.None,
            "InitialAnimationStarting": animateFadeDown, // Instead, animate with this function

            nodeTemplateMap: self.myDiagram.nodeTemplateMap,  // share the templates used by self.myDiagram
            model: new go.GraphLinksModel([  // specify the contents of the Palette
              { category: "Start", text: "Start" },
              { text: "Step" },
              { category: "Conditional", text: "???" },
              { category: "End", text: "End" },
              { category: "Comment", text: "Comment" }
            ])
          });

      // This is a re-implementation of the default animation, except it fades in from downwards, instead of upwards.
      function animateFadeDown(e) {
        var diagram = e.diagram;
        var animation = new go.Animation();
        animation.isViewportUnconstrained = true; // So Diagram positioning rules let the animation start off-screen
        animation.easing = go.Animation.EaseOutExpo;
        animation.duration = 900;
        // Fade "down", in other words, fade in from above
        animation.add(diagram, 'position', diagram.position.copy().offset(0, 200), diagram.position);
        animation.add(diagram, 'opacity', 0, 1);
        animation.start();
      }
       
self.initialized=true;            

  
},
    _getValue: function () {
            var $input = this.$el.find('input');

            var val = $input.val();
            

            return $input.val();


        },    
       
        load:function(){
        	var self=this;
          var show_value = self._formatValue(self.value) ? self.value : JSON.stringify(self.default)
           
        self.myDiagram.model = go.Model.fromJson(show_value);
    
        },
       
       
    
          _renderReadonly: function () {
            var self=this;
          var show_value = self._formatValue(self.value) ? self.value : JSON.stringify(self.default)
            //this.$el.find('input').val(show_value);
            //this.$el.css("background-color", show_value);
            self.myDiagram=null;
              //self.diag=null;
               setTimeout(function(){
                if(self.diag != null){
                     self.diag.model = go.Model.fromJson(show_value);

                }
                else {
               self.simple_go();
                     self.diag.model = go.Model.fromJson(show_value);

                }

                setTimeout(function(){
                  self.$('img').remove();
                self.$('#img').after(self.diag.makeImage({
                  size: new go.Size(NaN,600)
                }))
                },1500);
                },2500)
            
        },

         _renderEdit: function () {

               var self=this;
          var show_value = self._formatValue(self.value) ? self.value : JSON.stringify(self.default)
            this.$el.find('input').val(show_value);
           
                
           
              
                  setTimeout(function(){
                if(self.myDiagram != null)  { 
               
        
               self.load();
                                // self.initialized=false;

              }
          else {
                 self.init_go();

              }
                           
              },2500)
            

        },
        
    });

    field_registry.add('field_flow_chart', FieldFlowChart);
 return {
        FieldFlowChart: FieldFlowChart
    };
 
    
});
