# **ledo\_ontology\_core Final Project Structure v1.1**

ledo\_ontology\_core/  
  AGENTS.md  
  README.md  
  pyproject.toml  
  .gitignore

  templates/  
    implementation\_guide\_template.md  
    spec\_metadata\_template.md  
    codex\_task\_prompt\_template.md

  00\_master\_architecture/  
    unified\_cyber\_physical\_core.md  
    implementation\_guide.md

  01\_layer\_architecture/  
    layered\_semantic\_architecture.md  
    implementation\_guide.md

  02\_stack\_blueprint/  
    README.md  
    technology\_stack\_blueprint.md  
    implementation\_guide.md

    01\_platform\_runtime\_devops\_stack/  
      platform\_runtime\_devops\_stack.md  
      implementation\_guide.md

    02\_ontology\_semantic\_reasoning\_stack/  
      ontology\_semantic\_reasoning\_stack.md  
      implementation\_guide.md

    03\_data\_ingestion\_mapping\_stack/  
      data\_ingestion\_mapping\_stack.md  
      implementation\_guide.md

    04\_storage\_knowledge\_memory\_stack/  
      storage\_knowledge\_memory\_stack.md  
      implementation\_guide.md

    05\_streaming\_messaging\_stack/  
      streaming\_messaging\_stack.md  
      implementation\_guide.md

    06\_api\_service\_integration\_stack/  
      api\_service\_integration\_stack.md  
      implementation\_guide.md

    07\_agent\_llm\_orchestration\_stack/  
      agent\_llm\_orchestration\_stack.md  
      implementation\_guide.md

    08\_policy\_security\_governance\_stack/  
      policy\_security\_governance\_stack.md  
      implementation\_guide.md

    09\_runtime\_validation\_safety\_stack/  
      runtime\_validation\_safety\_stack.md  
      implementation\_guide.md

    10\_execution\_adapter\_cps\_stack/  
      execution\_adapter\_cps\_stack.md  
      implementation\_guide.md

    11\_observability\_audit\_trace\_stack/  
      observability\_audit\_trace\_stack.md  
      implementation\_guide.md

    12\_ui\_graph\_digital\_twin\_stack/  
      ui\_graph\_digital\_twin\_stack.md  
      implementation\_guide.md

  03\_core\_specifications/  
    README.md

    01\_common\_schema\_dto/  
      common\_schema\_dto.md  
      implementation\_guide.md

    02\_event\_type\_taxonomy/  
      event\_type\_taxonomy.md  
      implementation\_guide.md

    03\_action\_type\_registry/  
      action\_type\_registry.md  
      implementation\_guide.md

    04\_state\_model\_registry/  
      state\_model\_registry.md  
      implementation\_guide.md

    05\_evidence\_model/  
      evidence\_model.md  
      implementation\_guide.md

    06\_ontology\_module\_boundary/  
      ontology\_module\_boundary.md  
      implementation\_guide.md

    07\_decision\_approval\_matrix/  
      decision\_approval\_matrix.md  
      implementation\_guide.md

    08\_policy\_governance\_model/  
      policy\_governance\_model.md  
      implementation\_guide.md

    09\_execution\_adapter\_model/  
      execution\_adapter\_model.md  
      implementation\_guide.md

    10\_audit\_observability\_model/  
      audit\_observability\_model.md  
      implementation\_guide.md

  04\_domain\_ontology\_modules/  
    README.md

    core\_upper/  
      core\_upper\_ontology.md  
      implementation\_guide.md

    core\_crosscutting/  
      core\_crosscutting\_ontology.md  
      implementation\_guide.md

    construction/  
      construction\_ontology.md  
      implementation\_guide.md

    industrial/  
      industrial\_ontology.md  
      implementation\_guide.md

    robot/  
      robot\_ontology.md  
      implementation\_guide.md

    policy/  
      policy\_ontology.md  
      implementation\_guide.md

    ai/  
      ai\_ontology.md  
      implementation\_guide.md

    evidence/  
      evidence\_ontology.md  
      implementation\_guide.md

    event/  
      event\_ontology.md  
      implementation\_guide.md

    state/  
      state\_ontology.md  
      implementation\_guide.md

    action/  
      action\_ontology.md  
      implementation\_guide.md

    mapping/  
      mapping\_ontology.md  
      implementation\_guide.md

  05\_registry\_specs/  
    README.md

    event\_registry/  
      event\_registry.md  
      implementation\_guide.md

    action\_registry/  
      action\_registry.md  
      implementation\_guide.md

    state\_registry/  
      state\_registry.md  
      implementation\_guide.md

    evidence\_registry/  
      evidence\_registry.md  
      implementation\_guide.md

    decision\_registry/  
      decision\_registry.md  
      implementation\_guide.md

    approval\_registry/  
      approval\_registry.md  
      implementation\_guide.md

    policy\_registry/  
      policy\_registry.md  
      implementation\_guide.md

  06\_runtime\_validation/  
    README.md

    shacl\_shapes/  
      shacl\_shapes.md  
      implementation\_guide.md

    validators/  
      runtime\_validators.md  
      implementation\_guide.md

    safety\_gate/  
      safety\_gate.md  
      implementation\_guide.md

    toctou/  
      toctou\_validation.md  
      implementation\_guide.md

    idempotency/  
      idempotency\_validation.md  
      implementation\_guide.md

    network\_health/  
      network\_health\_validation.md  
      implementation\_guide.md

  07\_implementation\_plan/  
    README.md

    mvp\_phase\_1/  
      mvp\_phase\_1\_plan.md

    mvp\_phase\_2/  
      mvp\_phase\_2\_plan.md

    mvp\_phase\_3/  
      mvp\_phase\_3\_plan.md

  08\_appendices/  
    README.md

    appendix\_a\_stack\_catalog/  
      stack\_catalog.md

    appendix\_b\_event\_catalog/  
      event\_catalog.md

    appendix\_c\_state\_catalog/  
      state\_catalog.md

    appendix\_d\_evidence\_catalog/  
      evidence\_catalog.md

    appendix\_e\_ontology\_module\_catalog/  
      ontology\_module\_catalog.md

    appendix\_f\_decision\_approval\_catalog/  
      decision\_approval\_catalog.md

  09\_archive/  
    drafts/  
    old\_versions/

  src/  
    ledo\_ontology\_core/  
      \_\_init\_\_.py

      framework/  
        \_\_init\_\_.py

        schemas/  
          \_\_init\_\_.py

        registries/  
          \_\_init\_\_.py

        validation/  
          \_\_init\_\_.py

        decision/  
          \_\_init\_\_.py

        policy/  
          \_\_init\_\_.py

        adapters/  
          \_\_init\_\_.py

        audit/  
          \_\_init\_\_.py

        graph/  
          \_\_init\_\_.py

      domain\_packs/  
        \_\_init\_\_.py

        construction/  
          \_\_init\_\_.py  
          classes.yaml  
          properties.yaml  
          event\_types.yaml  
          action\_types.yaml  
          state\_models.yaml  
          evidence\_rules.yaml  
          decision\_rules.yaml

        industrial/  
          \_\_init\_\_.py  
          classes.yaml  
          properties.yaml  
          event\_types.yaml  
          action\_types.yaml  
          state\_models.yaml  
          evidence\_rules.yaml  
          decision\_rules.yaml

        robot/  
          \_\_init\_\_.py  
          classes.yaml  
          properties.yaml  
          capabilities.yaml  
          mission\_states.yaml  
          event\_types.yaml  
          action\_types.yaml  
          evidence\_rules.yaml  
          decision\_rules.yaml

        policy/  
          \_\_init\_\_.py  
          roles.yaml  
          permissions.yaml  
          approval\_rules.yaml  
          policy\_rules.yaml

        mapping/  
          \_\_init\_\_.py  
          external\_schema\_mappings.yaml  
          ontology\_mappings.yaml

  tests/  
    unit/  
      framework/  
      domain\_packs/

    integration/  
      decision\_flow/  
      safety\_gate\_flow/  
      registry\_loading/  
      graph\_export/

    fixtures/  
      sample\_events/  
      sample\_evidence/  
      sample\_states/  
      sample\_domain\_packs/

