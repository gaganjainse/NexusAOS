from .host import register_host_tools
from .mind import register_mind_tools
from .ops import register_ops_tools
from .soma import register_soma_tools

TOOLSET_REGISTRARS = [
    register_soma_tools,
    register_mind_tools,
    register_ops_tools,
    register_host_tools,
]
