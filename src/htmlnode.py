class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError("Sorry, no time.")
    

    def props_to_html(self):
        if self.props == None:
            return ""
        return "".join(list(map(lambda prop: f' {prop[0]}="{prop[1]}"', self.props.items())))
        #Should turn this: {'href': 'http://www.sksturm.at', 'target': '_blank'} into this: " href="http://www.sksturm.at" target="_blank"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("No value given. The LeafNode must have a value")
        
        self_enclosing_tags = ["area","base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"]
        
        if self.tag == None:
            return f"{self.value}"
        if self.tag in self_enclosing_tags:
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag given. The ParentNode must have a tag.")
        
        if self.children == None:
            raise ValueError("ParentNode is missing value for children")
        
        children = ""

        for child in self.children:
                children += (child.to_html())

        return f'<{self.tag}{self.props_to_html()}>{children}</{self.tag}>'
        