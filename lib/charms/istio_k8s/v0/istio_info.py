"""TODO: Add a proper docstring here.

* using requirer:
    * handle info changed event  <-- suggest a charm test to confirm this?

* using provider:
    * handle send error
    * use the is_ready()

use the custom event

mention the things we import that might be useful to the user (events, etc)
"""
from typing import List, Optional, Union

from charm_relation_building_blocks.data_models import DatabagModel
from charm_relation_building_blocks.relation_handlers import Receiver, Sender
# import and re-export these classes from the relation_handlers module, in case the user needs them
from charm_relation_building_blocks.data_models import DataValidationError as DataValidationError  # ignore: F401
from charm_relation_building_blocks.relation_handlers import DataChangedEvent as DataChangedEvent  # ignore: F401
from charm_relation_building_blocks.relation_handlers import ReceiverCharmEvents as ReceiverCharmEvents  # ignore: F401

from ops import CharmBase, BoundEvent
from pydantic import BaseModel, Field

# The unique Charmhub library identifier, never change it
LIBID = "17dff53d5bf649f29614365bde32451b"

# Increment this major API version when introducing breaking changes
LIBAPI = 0

# Increment this PATCH version before using `charmcraft publish-lib` or reset
# to 0 if you are raising the major API version
LIBPATCH = 1

DEFAULT_RELATION_NAME = "istio-info"


# Interface schema

class IstioInfoAppData(DatabagModel, BaseModel):
    """Data model for the istio-info interface."""

    root_namespace: str = Field(
        description="The root namespace for the Istio installation.",
        examples=["istio-system"],
    )


class IstioInfoRequirer(Receiver):
    """Class for handling the receiver side of the istio-info relation."""

    # inherits the events:
    # on = ReceiverCharmEvents()  # type: ignore[reportAssignmentType]
    #

    def __init__(
            self,
            charm: CharmBase,
            relation_name: str = DEFAULT_RELATION_NAME,
            refresh_event: Optional[Union[BoundEvent, List[BoundEvent]]] = None,
    ) -> None:
        """Initialize the IstioInfoRequirer object.

        Args:
            charm: The charm instance.
            relation_name: The name of the relation.
            refresh_event: An event or list of events that should trigger the library to process its relations.
                           By default, this charm already observes the relation_changed event.
        """
        super().__init__(charm, relation_name, IstioInfoAppData, refresh_event)


class IstioInfoProvider(Sender):
    """Class for handling the sending side of the istio-info relation."""

    def __init__(
            self,
            charm: CharmBase,
            root_namespace: str,
            relation_name: str = DEFAULT_RELATION_NAME,
            refresh_event: Optional[Union[BoundEvent, List[BoundEvent]]] = None,
    ) -> None:
        """Initialize the IstioInfoProvider object.

        Args:
            charm: The charm instance.
            root_namespace: The root namespace for the Istio installation.
            relation_name: The name of the relation.
            refresh_event: An event or list of events that should trigger the library to publish data to its relations.
                           By default, this charm already observes the relation_joined and on_leader_elected events.
        """
        data = IstioInfoAppData(root_namespace=root_namespace)
        super().__init__(charm, data, relation_name, refresh_event)
